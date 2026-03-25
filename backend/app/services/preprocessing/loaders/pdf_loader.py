import fitz


def extract_pdf(path: str) -> str:
    doc = fitz.open(path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text