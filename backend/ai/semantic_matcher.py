from sentence_transformers import SentenceTransformer, util

# Lightweight but powerful model
model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_match(cv_text: str, job_text: str):
    """
    Compute semantic similarity between CV and Job Description
    """

    cv_embedding = model.encode(cv_text, convert_to_tensor=True)
    job_embedding = model.encode(job_text, convert_to_tensor=True)

    similarity = util.cos_sim(cv_embedding, job_embedding).item()

    score = int(similarity * 100)

    if score > 80:
        verdict = "Excellent Match"
    elif score > 60:
        verdict = "Good Match"
    elif score > 40:
        verdict = "Partial Match"
    else:
        verdict = "Weak Match"

    return {
        "semantic_score": score,
        "verdict": verdict
    }
