from fastapi import FastAPI, UploadFile, File, Form
from dotenv import load_dotenv

import os
import tempfile

from backend.cv_parser import extract_text_from_pdf
from backend.ai.skill_extractor import extract_skills
from backend.ai.profile_builder import build_profile
from backend.ai.job_matcher import calculate_match
from backend.ai.career_recommender import rank_careers
from backend.ai.semantic_matcher import semantic_match
from backend.ai.career_coach import generate_career_advice
from backend.ai.career_chat import career_chat

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

app = FastAPI(
    title="CareerPilot AI",
    version="1.0.0"
)

TEMP_DIR = tempfile.gettempdir()


@app.get("/")
def root():
    return {"message": "CareerPilot AI is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


# =========================
# CV UPLOAD + PARSING
# =========================
@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=TEMP_DIR) as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    text = extract_text_from_pdf(file_path)

    skills = extract_skills(text)
    profile = build_profile(text)

    os.remove(file_path)

    return {
        "filename": file.filename,
        "skills": skills,
        "profile": profile
    }


# =========================
# JOB MATCHING
# =========================
@app.post("/match-job")
async def match_job(
    file: UploadFile = File(...),
    job_description: str = Form("")
):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=TEMP_DIR) as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    cv_text = extract_text_from_pdf(file_path)

    skills = extract_skills(cv_text)
    profile = build_profile(cv_text)

    match_result = calculate_match(
        cv_text,
        job_description,
        skills
    )

    os.remove(file_path)

    return {
        "profile": profile,
        "match": match_result
    }


# =========================
# CAREER RECOMMENDATION
# =========================
@app.post("/career-recommend")
async def career_recommend(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=TEMP_DIR) as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    cv_text = extract_text_from_pdf(file_path)

    skills = extract_skills(cv_text)
    profile = build_profile(cv_text)

    jobs = [
        {"title": "Backend Developer", "skills": [
            "python", "fastapi", "docker"]},
        {"title": "Data Engineer", "skills": ["sql", "python", "aws"]},
        {"title": "ML Engineer", "skills": [
            "python", "nlp", "machine learning"]}
    ]

    recommendation = rank_careers(cv_text, skills, jobs)

    os.remove(file_path)

    return {
        "profile": profile,
        "recommendation": recommendation
    }


# =========================
# SEMANTIC MATCHING (AI)
# =========================
@app.post("/semantic-match")
async def semantic_match_api(
    file: UploadFile = File(...),
    job_description: str = Form("")
):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=TEMP_DIR) as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    cv_text = extract_text_from_pdf(file_path)

    result = semantic_match(cv_text, job_description)

    os.remove(file_path)

    return {"result": result}


# =========================
# FULL AI PIPELINE
# =========================
@app.post("/career-ai")
async def career_ai(
    file: UploadFile = File(...),
    job_description: str = Form("")
):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=TEMP_DIR) as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    cv_text = extract_text_from_pdf(file_path)

    skills = extract_skills(cv_text)
    profile = build_profile(cv_text)

    match_result = calculate_match(cv_text, job_description, skills)

    career_plan = recommend_careers(
        skills,
        match_result["match_score"]
    )

    semantic_result = semantic_match(cv_text, job_description)

    advice = generate_career_advice(profile, match_result)

    os.remove(file_path)

    return {
        "profile": profile,
        "match": match_result,
        "semantic": semantic_result,
        "career_plan": career_plan,
        "career_coach": advice
    }


# =========================
# CAREER CHAT AI
# =========================
@app.post("/career-chat")
async def career_chat_api(
    question: str = Form(...),
    file: UploadFile = File(...)
):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=TEMP_DIR) as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    cv_text = extract_text_from_pdf(file_path)

    skills = extract_skills(cv_text)
    profile = build_profile(cv_text)

    job_description = "software engineer backend python fastapi"

    match_result = calculate_match(cv_text, job_description, skills)

    advice = generate_career_advice(profile, match_result)

    response = career_chat(question, profile, match_result, advice)

    os.remove(file_path)

    return {"answer": response}
