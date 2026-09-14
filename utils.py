import hashlib


def hash_text(text: str):
    return hashlib.sha256(text.encode()).hexdigest()


def clean_description(description):
    if not isinstance(description, str):
        return ""

    cleaned = "\n".join(
        line for line in description.replace("\\", "").splitlines() if line.strip()
    )

    return " ".join(cleaned.lower().split())
