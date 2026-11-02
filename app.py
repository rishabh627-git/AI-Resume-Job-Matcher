import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from matcher import extract_text, match_resume_to_job, extract_skills

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-before-deployment")
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    job_description = ""
    if request.method == "POST":
        job_description = request.form.get("job_description", "").strip()
        uploaded = request.files.get("resume")
        if not job_description:
            flash("Please paste the job description.", "error")
        elif not uploaded or uploaded.filename == "":
            flash("Please choose a resume file.", "error")
        elif not allowed_file(uploaded.filename):
            flash("Supported formats: PDF, DOCX and TXT.", "error")
        else:
            safe_name = secure_filename(uploaded.filename)
            saved_path = UPLOAD_DIR / safe_name
            uploaded.save(saved_path)
            try:
                resume_text = extract_text(saved_path)
                result = match_resume_to_job(resume_text, job_description)
                result["filename"] = safe_name
                result["resume_skills"] = extract_skills(resume_text)
                result["job_skills"] = extract_skills(job_description)
                result["missing_skills"] = sorted(set(result["job_skills"]) - set(result["resume_skills"]))
            except Exception as exc:
                flash(f"Could not process this file: {exc}", "error")
            finally:
                try:
                    saved_path.unlink(missing_ok=True)
                except OSError:
                    pass
    return render_template("index.html", result=result, job_description=job_description)

@app.route("/health")
def health():
    return {"status": "ok", "service": "AI Resume Job Matcher"}

if __name__ == "__main__":
    app.run(debug=True)
