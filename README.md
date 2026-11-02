# MatchPoint — AI Resume–Job Matching System

A local Flask web app that compares a resume with a job description using TF-IDF and cosine similarity. It also extracts a practical skills list and highlights job-description keywords that may be absent from the resume.

## Features
- Upload PDF, DOCX or TXT resumes (8 MB maximum).
- Extract text from documents.
- Calculate a 0–100% textual similarity score.
- Identify skills from a configurable built-in keyword list.
- Show missing skills and job-description keywords to review.
- Responsive dashboard and health endpoint (`/health`).

## Technology
Python 3.11, Flask, scikit-learn, PyPDF, python-docx, HTML/CSS.

## Windows setup
1. Install Python 3.11 and tick **Add Python to PATH**.
2. Open this folder in VS Code.
3. In the terminal run:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and activate again. You can also run `run_windows.bat`.

4. Open `http://127.0.0.1:5000`.

## Notes and limitations
- TF-IDF cosine similarity measures overlap in document wording; it is not a semantic model and does not judge candidate quality.
- The skills dictionary is intentionally transparent and editable in `matcher.py`. Extend it for your target roles.
- Scanned/image-only PDFs need OCR; this version extracts embedded PDF text.
- Uploaded files are processed locally and deleted from the upload folder after analysis. Do not deploy with the development server or default secret key.
- This project is an educational decision-support demo, not an automated hiring decision system.

## Project structure
```text
AI_Resume_Job_Matcher/
├── app.py
├── matcher.py
├── requirements.txt
├── run_windows.bat
├── templates/index.html
├── static/style.css
└── uploads/.gitkeep
```
