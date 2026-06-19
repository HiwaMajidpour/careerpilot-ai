from fastapi import FastAPI, UploadFile, File
import tempfile
import os

from backend.cv_parser import extract_text_from_pdf
from backend.ai.skill_extractor import extract_skills
from backend.ai.profile_builder import build_profile
from backend.ai.job_matcher import calculate_match
from backend.ai.career_recommender import rank_careers
from backend.ai.semantic_matcher import semantic_match

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


@app.post("/match-job")
async def match_job(file: UploadFile = File(...), job_description: str = ""):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    text = extract_text_from_pdf(file_path)

    skills = extract_skills(text)
    profile = build_profile(text)

    match_result = calculate_match(text, job_description, skills)

    os.remove(file_path)

    return {
        "profile": profile,
        "match": match_result
    }


@app.post("/career-recommend")
async def career_recommend(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    text = extract_text_from_pdf(file_path)

    skills = extract_skills(text)
    profile = build_profile(text)

    jobs = [
        {"title": "Backend Developer", "skills": [
            "python", "fastapi", "docker"]},
        {"title": "Data Engineer", "skills": ["sql", "python", "aws"]},
        {"title": "ML Engineer", "skills": [
            "python", "nlp", "machine learning"]}
    ]

    recommendation = rank_careers(text, skills, jobs)

    os.remove(file_path)

    return {
        "profile": profile,
        "recommendation": recommendation
    }


@app.post("/semantic-match")
async def semantic_match_api(file: UploadFile = File(...), job_description: str = ""):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    cv_text = extract_text_from_pdf(file_path)

    result = semantic_match(cv_text, job_description)

    os.remove(file_path)

    return {
        "result": result
    }
