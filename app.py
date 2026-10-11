
import streamlit as st

from resume_analyzer import analyze_resume, extract_text_from_file

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer")
st.caption("Compare a resume against a job description and identify skill gaps.")

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

uploaded_resume = st.file_uploader(
    "Upload your resume",
    type=["txt", "pdf", "docx"],
    help="Supported formats: TXT, PDF, and DOCX.",
)

if uploaded_resume is not None:
    try:
        st.session_state.resume_text = extract_text_from_file(uploaded_resume)
    except Exception as exc:
        st.warning(f"Unable to read the uploaded file: {exc}")

resume = st.text_area(
    "Resume text",
    value=st.session_state.resume_text,
    height=250,
    placeholder="Paste your resume text here...",
)

job = st.text_area(
    "Job description",
    height=250,
    placeholder="Paste the job description here...",
)

if st.button("Analyze Resume", type="primary"):
    if not resume.strip() or not job.strip():
        st.warning("Please add both a resume and a job description before analyzing.")
    else:
        result = analyze_resume(resume, job)

        st.subheader("📊 Match Summary")
        st.metric("Skill Match Score", f"{result['score']}%")
        st.progress(min(result["score"], 100) / 100)
        st.info(result["summary"])

        col1, col2 = st.columns(2)

        with col1:
            st.success("✅ Matched skills")
            if result["matched_skills"]:
                st.write(", ".join(result["matched_skills"]))
            else:
                st.write("No matching skills found yet.")

        with col2:
            st.error("📌 Missing skills")
            if result["missing_skills"]:
                st.write(", ".join(result["missing_skills"]))
            else:
                st.write("No missing skills from the tracked skill list.")

        st.subheader("💡 Suggested next steps")
        if result["missing_skills"]:
            st.write(
                "Focus on improving these areas before applying: "
                + ", ".join(result["missing_skills"])
            )
        else:
            st.write(
                "Your resume covers the main skill areas in this job description. "
                "Consider tailoring the experience section and projects to make the match clearer."
            )
