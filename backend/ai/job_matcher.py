def calculate_match(cv_text: str, job_text: str, skills: list):

    cv_lower = cv_text.lower()
    job_lower = job_text.lower()

    job_skills = {
        "python", "fastapi", "django", "sql", "docker",
        "aws", "machine learning", "nlp", "git"
    }

    matched_skills = []
    missing_skills = []

    for skill in job_skills:
        if skill in cv_lower and skill in job_lower:
            matched_skills.append(skill)
        elif skill in job_lower and skill not in cv_lower:
            missing_skills.append(skill)

    score = int((len(matched_skills) / len(job_skills))
                * 100) if job_skills else 0

    if score > 80:
        recommendation = "Strong match for this role"
    elif score > 50:
        recommendation = "Moderate match – some gaps exist"
    else:
        recommendation = "Weak match – consider upskilling"

    return {
        "match_score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation
    }
