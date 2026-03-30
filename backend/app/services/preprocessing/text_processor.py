from app.services.preprocessing.nlp.spacy_pipeline import process_with_spacy

# 🔶 OPTIONAL (enable if needed)
from textblob import TextBlob


def process_text(text: str) -> dict:
    """
    Process text using spaCy pipeline
    Returns structured + normalized text for downstream layers
    """

    try:
        cleaned, tokens = process_with_spacy(text)

        # 🔥 OPTIONAL SPELL CORRECTION (OFF by default)
        corrected = str(TextBlob(cleaned).correct())

        normalized_text = corrected

        return {
            "original": text,
            "cleaned": cleaned,
            "tokens": tokens,

            # 🔥 CRITICAL FIELD (for normalization layer)
            "normalized_text": normalized_text
        }

    except Exception as e:
        # 🔥 FAIL-SAFE (VERY IMPORTANT IN PROD)
        return {
            "original": text,
            "cleaned": text,
            "tokens": text.split(),
            "normalized_text": text,
            "error": str(e)
        }