def calculate_score(skills, education):

    score = 0

    score += min(len(skills) * 10, 50)

    if education:
        score += 20

    if "python" in skills:
        score += 10

    if "machine learning" in skills:
        score += 10

    if "streamlit" in skills:
        score += 10

    return min(score, 100)