from resume_analyzer import analyze_resume, extract_skills


def test_extract_skills_recognizes_common_technical_terms():
    text = "Experienced Python developer with SQL, pandas, and AWS experience."
    skills = extract_skills(text)

    assert "python" in skills
    assert "sql" in skills
    assert "pandas" in skills
    assert "aws" in skills


def test_analyze_resume_returns_score_and_gap_summary():
    resume = "Python, SQL, pandas, machine learning, AWS, Git, communication"
    job = "We need Python, SQL, AWS, Docker, and machine learning"

    result = analyze_resume(resume, job)

    assert result["score"] >= 50
    assert "python" in result["matched_skills"]
    assert "docker" in result["missing_skills"]
    assert "summary" in result
