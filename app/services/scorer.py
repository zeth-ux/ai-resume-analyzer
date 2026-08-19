import re
from sentence_transformers import SentenceTransformer, util

ROLE_PROFILES = {
    "ai_software_engineer": {
        "title": "AI Software Engineer",
        "required_skills": ["python", "pytorch", "machine learning", "api", "docker"],
        "nice_to_have": ["fastapi", "aws", "kubernetes", "computer vision", "sql"],
    },
    "backend_engineer": {
        "title": "Backend Engineer",
        "required_skills": ["python", "sql", "api", "docker", "system design"],
        "nice_to_have": ["fastapi", "microservices", "aws", "redis", "postgresql"],
    },
    "data_scientist": {
        "title": "Data Scientist",
        "required_skills": ["python", "pandas", "statistics", "machine learning", "sql"],
        "nice_to_have": ["numpy", "visualization", "a/b testing", "tensorflow"],
    },
}

_model = SentenceTransformer("all-MiniLM-L6-v2")


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def keyword_score(resume_text: str, role_key: str) -> dict:
    if role_key not in ROLE_PROFILES:
        raise ValueError(f"Unknown role: {role_key}")

    profile = ROLE_PROFILES[role_key]
    cleaned = clean_text(resume_text)

    matched_required = [kw for kw in profile["required_skills"] if kw in cleaned]
    missing_required = [kw for kw in profile["required_skills"] if kw not in cleaned]
    matched_nice = [kw for kw in profile["nice_to_have"] if kw in cleaned]
    missing_nice = [kw for kw in profile["nice_to_have"] if kw not in cleaned]

    required_score = len(matched_required) / len(profile["required_skills"])
    nice_score = len(matched_nice) / len(profile["nice_to_have"]) if profile["nice_to_have"] else 0

    overall = round((required_score * 0.7 + nice_score * 0.3) * 100, 1)

    return {
        "role": profile["title"],
        "overall_keyword_score": overall,
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_nice_to_have": matched_nice,
        "missing_nice_to_have": missing_nice,
    }


def embedding_score(resume_text: str, role_key: str) -> dict:
    if role_key not in ROLE_PROFILES:
        raise ValueError(f"Unknown role: {role_key}")

    profile = ROLE_PROFILES[role_key]

    role_description = (
        f"{profile['title']} requiring skills in: "
        + ", ".join(profile["required_skills"] + profile["nice_to_have"])
    )

    resume_embedding = _model.encode(resume_text, convert_to_tensor=True)
    role_embedding = _model.encode(role_description, convert_to_tensor=True)

    similarity = util.cos_sim(resume_embedding, role_embedding).item()
    similarity_pct = round(max(0, min(1, similarity)) * 100, 1)

    return {
        "semantic_similarity_score": similarity_pct
    }