def recommend_careers(skills: list, match_score: int):

    recommendations = []

    skills_lower = [skill.lower() for skill in skills]

    # Backend Developer
    if "python" in skills_lower or "fastapi" in skills_lower:
        recommendations.append("Backend Developer")

    # Data Scientist
    if (
        "machine learning" in skills_lower
        or "nlp" in skills_lower
        or "deep learning" in skills_lower
    ):
        recommendations.append("Data Scientist")

    # DevOps Engineer
    if "docker" in skills_lower or "aws" in skills_lower:
        recommendations.append("DevOps Engineer")

    # Fallback recommendation
    if not recommendations:
        recommendations.append("Junior Software Engineer")

    learning_path = []

    if "docker" not in skills_lower:
        learning_path.append("Learn Docker")

    if "aws" not in skills_lower:
        learning_path.append("Learn AWS")

    if "git" not in skills_lower:
        learning_path.append("Master Git")

    return {
        "career_recommendations": recommendations,
        "learning_path": learning_path,
        "readiness_score": match_score
    }


def rank_careers(cv_text: str, skills: list, jobs: list):

    cv_lower = cv_text.lower()

    results = []

    for job in jobs:

        job_title = job["title"]
        job_skills = job["skills"]

        matched = 0

        for skill in job_skills:
            if skill.lower() in cv_lower:
                matched += 1

        score = (
            int((matched / len(job_skills)) * 100)
            if job_skills
            else 0
        )

        results.append({
            "job": job_title,
            "score": score
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    top_job = (
        results[0]["job"]
        if results
        else "Unknown"
    )

    missing_skills = []

    for job in jobs:
        for skill in job["skills"]:
            if skill.lower() not in cv_lower:
                missing_skills.append(skill)

    missing_skills = list(set(missing_skills))

    advice = (
        f"Focus on {', '.join(missing_skills[:3])} "
        f"to improve chances in {top_job}"
    )

    return {
        "top_matches": results,
        "career_advice": advice
    }
