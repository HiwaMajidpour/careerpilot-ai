def calculate_match(cv_text: str, job_text: str, skills: list):

    cv_lower = cv_text.lower()
    job_lower = job_text.lower()

    # Known skill dictionary (expandable)
    KNOWN_SKILLS = {
        "python",
        "fastapi",
        "django",
        "sql",
        "docker",
        "aws",
        "machine learning",
        "nlp",
        "git",
        "java"
    }

    # Extract job required skills from job description
    job_skills = []
    for skill in KNOWN_SKILLS:
        if skill in job_lower:
            job_skills.append(skill)

    # CV skills (from your extractor)
    cv_skills = set(skills)

    matched_skills = []
    missing_skills = []

    # Compare CV vs Job skills
    for skill in job_skills:
        if skill in cv_skills or skill in cv_lower:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    # Score calculation
    if len(job_skills) == 0:
        score = 0
    else:
        score = int((len(matched_skills) / len(job_skills)) * 100)

    # Recommendation logic
    if score >= 80:
        recommendation = "Strong match for this role"
    elif score >= 50:
        recommendation = "Moderate match – some gaps exist"
    else:
        recommendation = "Weak match – consider upskilling"

    return {
        "match_score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation
    }
