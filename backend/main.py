from fastapi import FastAPI, UploadFile, File
import tempfile

from backend.cv_parser import extract_text_from_pdf
from backend.ai.skill_extractor import extract_skills

app = FastAPI()


@app.get("/")
def root():
    return {"message": "CareerPilot AI is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):

    # Create temporary file (NO persistent storage)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    # Extract text from PDF
    text = extract_text_from_pdf(file_path)

    # Extract skills using AI/NLP
    skills = extract_skills(text)

    return {
        "filename": file.filename,
        "text_preview": text[:1000],
        "skills": skills
    }
