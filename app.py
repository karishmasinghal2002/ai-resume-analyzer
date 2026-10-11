
import streamlit as st
import re
from collections import Counter

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer & Job Matcher")
st.write("Analyze how well your resume matches a job description.")

SKILLS = [
    "python", "java", "javascript", "react", "node.js", "sql",
    "machine learning", "deep learning", "artificial intelligence",
    "data analysis", "pandas", "numpy", "tensorflow", "pytorch",
    "fastapi", "flask", "django", "html", "css", "git", "github",
    "rest api", "docker", "aws", "communication", "problem solving",
    "c++", "c", "excel", "power bi"
]

def extract_skills(text):
    text = text.lower()
    found = []
    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text):
            found.append(skill)
    return found

def analyze_resume(resume, job_description):
    resume_skills = set(extract_skills(resume))
    job_skills = set(extract_skills(job_description))

    if not job_skills:
        return None

    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    score = round(len(matched) / len(job_skills) * 100)

    return score, matched, missing

resume = st.text_area(
    "Paste your resume text",
    height=220,
    placeholder="Paste your education, skills, projects and experience..."
)

job = st.text_area(
    "Paste the job description",
    height=220,
    placeholder="Paste the skills and requirements from a job posting..."
)

if st.button("Analyze Resume", type="primary"):
    if not resume.strip() or not job.strip():
        st.warning("Please enter both your resume and the job description.")
    else:
        result = analyze_resume(resume, job)

        if result is None:
            st.warning("No supported skills found in the job description. Try adding technical skills.")
        else:
            score, matched, missing = result

            st.subheader("📊 Analysis Results")
            st.metric("Job Skill Match Score", f"{score}%")
            st.progress(score / 100)

            col1, col2 = st.columns(2)

            with col1:
                st.success("✅ Matched Skills")
                if matched:
                    st.write(", ".join(matched))
                else:
                    st.write("No matching skills found.")

            with col2:
                st.error("📌 Missing Skills")
                if missing:
                    st.write(", ".join(missing))
                else:
                    st.write("No missing skills from our current skill list!")

            st.info(
                "This is a rule-based skill match score, not an official ATS score "
                "or a prediction of whether you will get hired."
            )

            st.subheader("💡 Suggested Next Steps")
            if missing:
                st.write(
                    "Review these job requirements and learn the relevant skills: "
                    + ", ".join(missing)
                )
            else:
                st.write(
                    "Your listed skills match the supported skills in this job description. "
                    "Review the required experience and project expectations too."
                )
