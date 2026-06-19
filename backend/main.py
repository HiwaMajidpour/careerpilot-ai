from fastapi import FastAPI, UploadFile, File
import tempfile
import os

from backend.cv_parser import extract_text_from_pdf
from backend.ai.skill_extractor import extract_skills
from backend.ai.profile_builder import build_profile

app = FastAPI()

# System temporary directory (safe for production)
TEMP_DIR = tempfile.gettempdir()


@app.get("/")
def root():
    return {"message": "CareerPilot AI is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):

    # Create temporary file (no persistent storage)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=TEMP_DIR) as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    # Extract text from PDF
    text = extract_text_from_pdf(file_path)

    # AI processing
    skills = extract_skills(text)
    profile = build_profile(text)

    # Cleanup temp file
    os.remove(file_path)

    return {
        "filename": file.filename,
        "skills": skills,
        "profile": profile
    }
