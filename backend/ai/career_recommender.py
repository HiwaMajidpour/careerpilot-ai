def rank_careers(cv_text: str, skills: list, jobs: list):

    cv_lower = cv_text.lower()

    results = []

    for job in jobs:

        job_title = job["title"]
        job_skills = job["skills"]

        matched = 0
        missing = 0

        for skill in job_skills:
            if skill.lower() in cv_lower:
                matched += 1
            else:
                missing += 1

        if len(job_skills) == 0:
            score = 0
        else:
            score = int((matched / len(job_skills)) * 100)

        results.append({
            "job": job_title,
            "score": score
        })

    # Sort best matches
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    # AI-like advice logic
    top_job = results[0]["job"] if results else "Unknown"

    all_missing = []
    for job in jobs:
        for skill in job["skills"]:
            if skill.lower() not in cv_lower:
                all_missing.append(skill)

    unique_missing = list(set(all_missing))

    advice = f"Focus on {', '.join(unique_missing[:3])} to improve chances in {top_job}"

    return {
        "top_matches": results,
        "career_advice": advice
    }
