def generate_career_advice(profile: dict, match_result: dict):

    skills = profile.get("skills", [])
    score = match_result.get("match_score", 0)
    missing = match_result.get("missing_skills", [])

    # --- Explanation logic ---
    if score > 80:
        status = "You are a strong candidate for this role."
    elif score > 50:
        status = "You are a moderate fit, but need improvements."
    else:
        status = "You currently need significant upskilling."

    # --- Roadmap generation ---
    roadmap = []

    if "docker" in missing:
        roadmap.append("Learn Docker basics for deployment")

    if "aws" in missing:
        roadmap.append("Learn AWS fundamentals (EC2, S3)")

    if "sql" in missing:
        roadmap.append("Strengthen SQL and database design")

    if "fastapi" in missing:
        roadmap.append("Build 2 FastAPI projects")

    # --- AI summary ---
    summary = f"""
    Based on your profile, your strongest area is {skills[:3]}.
    Your match score is {score}%.

    {status}
    """

    return {
        "explanation": status,
        "roadmap": roadmap,
        "ai_summary": summary.strip()
    }
