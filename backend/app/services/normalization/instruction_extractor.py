from difflib import get_close_matches

ACTIONS = [
    "summarize", "explain", "analyze", "describe", "define",
    "translate", "convert", "classify", "extract", "detect",
    "compare", "evaluate", "predict", "recommend", "generate",
    "rewrite", "simplify", "expand",
    "transcribe"
]

CONVERSATION = ["hi", "hello", "hey", "how are you", "what's up"]


def find_action(word):
    match = get_close_matches(word, ACTIONS, n=1, cutoff=0.8)
    return match[0] if match else None


def is_conversation(text):
    return text.strip().lower() in CONVERSATION


def normalize_content(content):
    if isinstance(content, dict):
        return (
            content.get("original")
            or content.get("cleaned")
            or content.get("normalized_text")
            or str(content)
        )

    if isinstance(content, list):
        return " ".join(
            str(x.get("text", x)) if isinstance(x, dict) else str(x)
            for x in content
        )

    return str(content)


def extract_instruction(data: dict):

    processed = data.get("processed_data", {})
    raw_items = processed.get("data", [])

    text_input = ""
    original_text = ""

    # =========================
    # GET TEXT INPUT
    # =========================
    for item in raw_items:
        if item.get("metadata", {}).get("source") == "text":
            original_text = normalize_content(item.get("content", ""))
            text_input = original_text.lower().strip()
            break

    if not text_input:
        return {
            "text": "",
            "raw_text": "",
            "type": "default",
            "data_part": None,
            "source": "default"
        }

    # =========================
    # CONVERSATION
    # =========================
    if is_conversation(text_input):
        return {
            "text": "conversation",
            "raw_text": original_text,
            "type": "conversation",
            "data_part": text_input,
            "source": "text"
        }

    # =========================
    # SMART ACTION DETECTION
    # =========================
    if "summarize" in text_input:
        return {"text": "summarize", "raw_text": original_text, "type": "instruction_only", "data_part": None, "source": "text"}

    if "explain" in text_input or text_input.startswith(("what", "why", "how")):
        return {"text": "explain", "raw_text": original_text, "type": "instruction_only", "data_part": None, "source": "text"}

    if "convert" in text_input or "to audio" in text_input or "to text" in text_input:
        return {"text": "convert", "raw_text": original_text, "type": "instruction_only", "data_part": None, "source": "text"}

    # =========================
    # FALLBACK
    # =========================
    return {
        "text": text_input,
        "raw_text": original_text,
        "type": "raw_text",
        "data_part": None,
        "source": "text"
    }