import spacy

nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = {
    "python", "java", "sql", "fastapi", "machine learning",
    "deep learning", "nlp", "docker", "aws", "git"
}


def extract_skills(text: str):
    doc = nlp(text.lower())

    found = set()

    # 1. rule-based extraction (fast)
    for word in text.lower().split():
        if word in SKILL_KEYWORDS:
            found.add(word)

    # 2. NLP noun extraction (smarter)
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            if len(token.text) > 2:
                found.add(token.text)

    return list(found)
