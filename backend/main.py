from fastapi import FastAPI, UploadFile, File
import os

from backend.cv_parser import extract_text_from_pdf
from backend.ai.skill_extractor import extract_skills


app = FastAPI(
    title="CareerPilot AI",
    version="0.1.0"
)

UPLOAD_DIR = "uploads"


@app.get("/")
def root():
    return {
        "message": "CareerPilot AI is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================
# CV Upload + Parsing API
# =========================
@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # save file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # extract text
    text = extract_text_from_pdf(file_path)

    # extract skills (AI part)
    skills = extract_skills(text)

    return {
        "filename": file.filename,
        "text_preview": text[:1000],
        "skills": skills
    }
