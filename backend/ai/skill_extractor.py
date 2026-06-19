import spacy

SKILL_KEYWORDS = {
    "python", "java", "sql", "fastapi", "machine learning",
    "deep learning", "nlp", "docker", "aws", "git"
}

# Load spaCy model safely
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None


def extract_skills(text: str):
    text_lower = text.lower()
    found = set()

    # 1. Keyword matching (most reliable)
    for skill in SKILL_KEYWORDS:
        if skill in text_lower:
            found.add(skill)

    # 2. NLP enhancement (only if model exists)
    if nlp:
        doc = nlp(text_lower)

        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.strip()

            if chunk_text in SKILL_KEYWORDS:
                found.add(chunk_text)

    return list(found)
