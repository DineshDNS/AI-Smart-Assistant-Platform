from difflib import get_close_matches

ACTIONS = [
    "summarize", "explain", "analyze", "describe", "define",
    "translate", "convert", "classify", "extract", "detect",
    "compare", "evaluate", "predict", "recommend", "generate",
    "calculate", "compute", "estimate", "measure",
    "read", "parse", "process", "review", "scan", "interpret",
    "rewrite", "simplify", "improve", "expand", "shorten",
    "format", "clean", "normalize",
    "answer", "solve", "clarify", "justify", "elaborate",
    "identify", "recognize", "label", "segment",
    "transcribe", "listen",
    "tell", "show", "give", "list"
]

CONVERSATION = [
    "hi", "hello", "hey", "how are you", "what's up"
]

SEPARATORS = [":", "-", "->", "=>"]


def find_action(word):
    # 🔥 safer fuzzy match
    match = get_close_matches(word, ACTIONS, n=1, cutoff=0.85)
    return match[0] if match else None


def is_conversation(text):
    return text.strip().lower() in CONVERSATION


def extract_instruction(data: dict):

    processed = data.get("processed_data", {})
    text_data = processed.get("text")

    if text_data:
        text = text_data.get("original", "").strip().lower()

        # Normalize spacing
        text = text.replace(" :", ":").replace(": ", ":")

        if not text:
            return {
                "text": "",
                "type": "default",
                "data_part": None,
                "source": "default"
            }

        # =========================
        # CONVERSATION
        # =========================
        if is_conversation(text):
            return {
                "text": text,
                "type": "conversation",
                "data_part": text,
                "source": "text"
            }

        words = text.split()

        # =========================
        # 🔥 LONG TEXT → ALWAYS RAW
        # =========================
        if len(words) > 3:
            return {
                "text": text,
                "type": "raw_text",
                "data_part": None,
                "source": "text"
            }

        # =========================
        # STRUCTURED INPUT
        # =========================
        for sep in SEPARATORS:
            if sep in text:
                left, right = text.split(sep, 1)

                left = left.strip()
                right = right.strip()

                action = find_action(left)

                if action:
                    return {
                        "text": action,
                        "type": "instruction_data",
                        "data_part": right,
                        "source": "text"
                    }

        # =========================
        # 🔥 SHORT COMMAND ONLY
        # =========================
        for w in words:
            action = find_action(w)
            if action:
                return {
                    "text": action,
                    "type": "instruction_only",
                    "data_part": None,
                    "source": "text"
                }

        # =========================
        # DEFAULT → RAW TEXT
        # =========================
        return {
            "text": text,
            "type": "raw_text",
            "data_part": None,
            "source": "text"
        }

    return {
        "text": "",
        "type": "default",
        "data_part": None,
        "source": "default"
    }