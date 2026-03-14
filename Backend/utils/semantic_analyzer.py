def detect_project_domain(analysis: dict) -> str:
    text = str(analysis).lower()

    rules = {
        "authentication system": ["login", "signup", "jwt", "token", "auth"],
        "file sharing platform": ["upload", "download", "file", "storage"],
        "video platform": ["video", "stream", "watch"],
        "e-learning platform": ["course", "lesson", "quiz", "test"],
        "notes management system": ["notes", "subject", "chapter"],
        "database driven web application": ["model", "schema", "database"],
        "api service": ["route", "endpoint", "request", "response"]
    }

    detected = []
    for domain, keywords in rules.items():
        for k in keywords:
            if k in text:
                detected.append(domain)
                break

    if not detected:
        return "software management system"

    return ", ".join(detected)


def detect_features(analysis: dict):
    text = str(analysis).lower()
    features = []

    if "login" in text or "signup" in text:
        features.append("User Authentication")

    if "upload" in text:
        features.append("Content Upload")

    if "download" in text:
        features.append("Content Retrieval")

    if "jwt" in text:
        features.append("Token Based Security")

    if "model" in text:
        features.append("Database Storage")

    if "route" in text:
        features.append("REST API Endpoints")

    return features


def semantic_summary(project_name: str, analysis: dict) -> dict:
    return {
        "project_name": project_name,
        "detected_domain": detect_project_domain(analysis),
        "detected_features": detect_features(analysis),
        "raw_analysis": analysis
    }
