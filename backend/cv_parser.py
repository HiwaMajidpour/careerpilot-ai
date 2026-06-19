import pdfplumber
from backend.ai.skill_extractor import extract_skills


def extract_text_from_pdf(file_path: str):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def parse_cv(file_path: str):
    text = extract_text_from_pdf(file_path)

    skills = extract_skills(text)

    return {
        "raw_text": text,
        "skills": skills
    }
