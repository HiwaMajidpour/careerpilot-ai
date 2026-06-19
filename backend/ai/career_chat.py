def career_chat(user_question: str, profile: dict, match: dict, advice: dict):

    question = user_question.lower()

    skills = profile.get("skills", [])
    score = match.get("match_score", 0)
    roadmap = advice.get("roadmap", [])

    # --- Intent detection (simple but effective) ---
    if "why" in question or "why" in question:
        return f"""
Your score is {score}% because your CV partially matches required job skills.
Key missing areas are: {', '.join(match.get('missing_skills', [])[:3])}.
"""

    if "what should i learn" in question or "learn" in question:
        return f"""
You should focus on:
{chr(10).join(roadmap[:5])}
"""

    if "job" in question:
        return f"""
Based on your profile, your strongest direction is:
Backend / Data roles using skills: {', '.join(skills[:5])}
"""

    return f"""
I analyzed your profile. Your current match score is {score}%.
Ask me about skills, job fit, or career roadmap.
"""
