import io
import re
import unicodedata

try:
    from PyPDF2 import PdfReader
except ImportError:  # pragma: no cover
    PdfReader = None

try:
    from docx import Document
except ImportError:  # pragma: no cover
    Document = None


SKILL_ALIASES = {
    "python": ["python", "python developer", "python programming"],
    "sql": ["sql", "postgresql", "mysql", "database", "sqlite"],
    "pandas": ["pandas", "dataframe", "data analysis"],
    "aws": ["aws", "amazon web services", "ec2", "s3", "lambda"],
    "docker": ["docker", "containerization", "kubernetes", "k8s"],
    "machine learning": ["machine learning", "ml", "ai", "artificial intelligence"],
    "javascript": ["javascript", "js", "es6"],
    "react": ["react", "reactjs", "react.js"],
    "node.js": ["node.js", "nodejs", "node js"],
    "fastapi": ["fastapi", "fast api"],
    "flask": ["flask"],
    "git": ["git", "github", "version control"],
    "excel": ["excel", "microsoft excel"],
    "power bi": ["power bi", "powerbi"],
    "communication": ["communication", "stakeholder communication", "presentations"],
    "problem solving": ["problem solving", "debugging", "troubleshooting"],
    "data analysis": ["data analysis", "analytics", "business intelligence"],
    "java": ["java"],
    "c++": ["c++", "cpp"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "rest api": ["rest api", "restful api", "apis"],
}


def normalize_text(text):
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text.lower())
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9+#.]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_skills(text):
    if not text:
        return []

    normalized_text = normalize_text(text)
    found = []

    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = r"(?<![a-z0-9])" + re.escape(normalize_text(alias)) + r"(?![a-z0-9])"
            if re.search(pattern, normalized_text):
                found.append(skill)
                break

    return found


def analyze_resume(resume, job_description):
    if not resume or not job_description:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "summary": "Add both a resume and a job description to calculate a match score.",
        }

    resume_skills = set(extract_skills(resume))
    job_skills = set(extract_skills(job_description))

    if not job_skills:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "summary": "No supported skills were detected in the job description.",
        }

    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    score = round((len(matched) / len(job_skills)) * 100) if job_skills else 0

    if score >= 80:
        summary = "Strong match: your experience aligns well with the role requirements."
    elif score >= 50:
        summary = "Moderate match: you have several relevant skills, with a few gaps to close."
    else:
        summary = "Early match: focus on the missing skills and role-specific experience."

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "summary": summary,
    }


def extract_text_from_file(uploaded_file):
    if uploaded_file is None:
        return ""

    filename = getattr(uploaded_file, "name", "").lower()
    content = uploaded_file.read()

    if filename.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")

    if filename.endswith(".pdf"):
        if PdfReader is None:
            raise RuntimeError("PyPDF2 is required to read PDF files.")

        pdf = PdfReader(io.BytesIO(content))
        pages = []
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages.append(text)
        return "\n".join(pages)

    if filename.endswith(".docx"):
        if Document is None:
            raise RuntimeError("python-docx is required to read DOCX files.")

        doc = Document(io.BytesIO(content))
        paragraphs = [paragraph.text for paragraph in doc.paragraphs]
        return "\n".join(paragraphs)

    return content.decode("utf-8", errors="ignore")
