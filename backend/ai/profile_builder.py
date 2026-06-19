from backend.ai.skill_extractor import extract_skills


def build_profile(text: str):
    text_lower = text.lower()

    skills = extract_skills(text)

    # Simple heuristic for experience level
    if any(word in text_lower for word in ["senior", "lead", "architect"]):
        level = "senior"
    elif any(word in text_lower for word in ["junior", "intern", "entry"]):
        level = "junior"
    else:
        level = "mid"

    # Simple summary generator
    summary = text[:300].strip()

    return {
        "skills": skills,
        "experience_level": level,
        "summary": summary,
        "keywords": list(set(text_lower.split()[:30]))
    }
