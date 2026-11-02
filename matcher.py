from pathlib import Path
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILL_KEYWORDS = {
    "python", "java", "javascript", "typescript", "c++", "sql", "mysql",
    "postgresql", "mongodb", "flask", "django", "fastapi", "react",
    "node.js", "html", "css", "git", "docker", "aws", "azure",
    "machine learning", "deep learning", "nlp", "tensorflow", "pytorch",
    "scikit-learn", "pandas", "numpy", "data analysis", "excel",
    "communication", "leadership", "problem solving", "rest api",
    "linux", "opencv", "keras", "computer vision"
}

def extract_text(path):
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        from docx import Document
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Unsupported document format")

def clean_text(text):
    return re.sub(r"\s+", " ", text or "").strip()

def extract_skills(text):
    normalized = clean_text(text).lower()
    found = []
    for skill in SKILL_KEYWORDS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, normalized):
            found.append(skill)
    return sorted(found)

def match_resume_to_job(resume_text, job_description):
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)
    if len(resume_text) < 20:
        raise ValueError("Not enough text was extracted. Try a text-based PDF or DOCX file.")
    if len(job_description) < 20:
        raise ValueError("Please provide a more detailed job description.")
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=12000)
    matrix = vectorizer.fit_transform([resume_text, job_description])
    score = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0] * 100)
    terms = vectorizer.get_feature_names_out()
    resume_vec = matrix[0].toarray()[0]
    job_vec = matrix[1].toarray()[0]
    important = sorted(
        [(terms[i], float(job_vec[i])) for i in range(len(terms)) if job_vec[i] > 0 and resume_vec[i] == 0],
        key=lambda item: item[1], reverse=True
    )[:12]
    return {
        "score": round(score, 1),
        "interpretation": "Strong textual overlap" if score >= 55 else ("Moderate textual overlap" if score >= 30 else "Low textual overlap"),
        "keywords_to_review": [term for term, _ in important]
    }
