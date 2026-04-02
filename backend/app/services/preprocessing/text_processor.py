from app.services.preprocessing.nlp.spacy_pipeline import process_with_spacy

# 🔶 OPTIONAL (use carefully)
from textblob import TextBlob


def process_text(text: str, enable_correction: bool = False) -> dict:
    """
    Process text using spaCy pipeline

    🔥 RULE:
    - NEVER break original text
    - NEVER remove keywords like 'to'
    - Preserve semantic meaning

    Returns structured + normalized text for downstream layers
    """

    try:
        # =========================
        # ORIGINAL TEXT (STRICTLY PRESERVED)
        # =========================
        original = text.strip()

        # =========================
        # SPACY CLEANING
        # =========================
        cleaned, tokens = process_with_spacy(original)

        # =========================
        # 🔥 SAFE NORMALIZATION
        # =========================
        # Only normalize spacing + casing
        normalized_text = " ".join(cleaned.lower().split())

        # =========================
        # 🔥 OPTIONAL SPELL CORRECTION (SAFE MODE)
        # =========================
        # ⚠️ Disabled by default because it breaks intent
        if enable_correction:
            try:
                corrected = str(TextBlob(normalized_text).correct())

                # 🔥 SAFETY CHECK (do not accept harmful changes)
                if len(corrected.split()) >= len(normalized_text.split()):
                    normalized_text = corrected
            except Exception:
                pass  # ignore correction errors safely

        # =========================
        # RETURN STRUCTURE
        # =========================
        return {
            "original": original,               # 🔥 ALWAYS TRUE USER INPUT
            "cleaned": cleaned,                # spaCy processed
            "tokens": tokens,
            "normalized_text": normalized_text  # safe normalized version
        }

    except Exception as e:
        # =========================
        # 🔥 FAIL-SAFE (PRODUCTION SAFE)
        # =========================
        return {
            "original": text,
            "cleaned": text,
            "tokens": text.split(),
            "normalized_text": text,
            "error": str(e)
        }