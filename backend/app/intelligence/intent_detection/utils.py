import re

def normalize_text(text: str) -> str:
    return text.lower().strip()

def split_text(text: str, separators: list):
    pattern = "|".join([re.escape(sep) for sep in separators])
    return [t.strip() for t in re.split(pattern, text) if t.strip()]