from app.services.preprocessing.nlp.spacy_pipeline import process_with_spacy


def process_text(text: str) -> dict:
    cleaned, tokens = process_with_spacy(text)

    return {
        "original": text,
        "cleaned": cleaned,
        "tokens": tokens
    }