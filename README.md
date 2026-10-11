# AI Resume Analyzer

A lightweight Streamlit app that compares a resume against a job description and highlights the matching and missing skills.

## Features
- Paste resume text directly into the app
- Upload a resume from TXT, PDF, or DOCX files
- Compare skills against a job description
- Score the resume based on matched job requirements
- View missing skills and suggested next steps

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run app.py
   ```

## Example usage
- Copy a resume into the "Resume text" area.
- Paste a job description into the "Job description" area.
- Click "Analyze Resume" to review the fit score, matched skills, and missing skills.

## Testing

```bash
pytest -q
```
