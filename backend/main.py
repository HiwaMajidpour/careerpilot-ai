from fastapi import FastAPI, UploadFile, File
import tempfile

from backend.cv_parser import extract_text_from_pdf
from backend.ai.skill_extractor import extract_skills

app = FastAPI()


@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):

    # Create a temporary file (avoids storing files in the repository)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    # Extract raw text from the uploaded PDF
    text = extract_text_from_pdf(file_path)

    # Extract skills using NLP-based extractor
    skills = extract_skills(text)

    return {
        "filename": file.filename,
        "text_preview": text[:1000],
        "skills": skills
    }
