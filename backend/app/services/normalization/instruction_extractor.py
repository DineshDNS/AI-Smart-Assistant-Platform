from difflib import get_close_matches

# =========================
# ACTION WORDS (REAL-WORLD COVERAGE)
# =========================
ACTIONS = [
    # Core NLP / LLM tasks
    "summarize", "explain", "analyze", "describe", "define",
    "translate", "convert", "classify", "extract", "detect",

    # Data / analysis
    "compare", "evaluate", "predict", "recommend", "generate",
    "calculate", "compute", "estimate", "measure",

    # File / processing
    "read", "parse", "process", "review", "scan", "interpret",

    # Transformation
    "rewrite", "simplify", "improve", "expand", "shorten",
    "format", "clean", "normalize",

    # Q&A / reasoning
    "answer", "solve", "clarify", "justify", "elaborate",

    # Vision / image
    "identify", "recognize", "label", "segment",

    # Audio
    "transcribe", "listen",

    # General
    "tell", "show", "give", "list"
]


# =========================
# CONVERSATION WORDS
# =========================
CONVERSATION = [
    # Greetings
    "hi", "hello", "hey", "hey there",
    "good morning", "good afternoon", "good evening",

    # Casual talk
    "how are you", "how are you doing",
    "what's up", "whats up",
    "how is it going", "how's it going",

    # Polite starters
    "can you help me", "could you help me",
    "i need help", "help me",

    # Small talk
    "nice to meet you", "glad to meet you",
    "how have you been",

    # Chat intent
    "let's chat", "talk to me", "just chatting"
]


# =========================
# SPLIT SEPARATORS
# =========================
SEPARATORS = [":", "-", "->", "=>"]


# =========================
# HELPERS
# =========================
def find_action(word):
    match = get_close_matches(word, ACTIONS, n=1, cutoff=0.75)
    return match[0] if match else None


def contains_action(text):
    words = text.split()
    return any(find_action(w) for w in words)


def is_conversation(text):
    return text.strip().lower() in CONVERSATION


# =========================
# MAIN FUNCTION
# =========================
def extract_instruction(data: dict):

    processed = data.get("processed_data", {})
    text_data = processed.get("text")
    audio_data = processed.get("audio_text", [])
    files = processed.get("file", [])
    images = processed.get("image", [])

    # =========================
    # 1. TEXT PRIORITY
    # =========================
    if text_data:
        text = text_data.get("original", "").strip().lower()

        if text:

            # 🔹 Conversation
            if is_conversation(text):
                return {
                    "text": "conversation",
                    "type": "conversation",
                    "data_part": text,
                    "source": "text"
                }

            # 🔹 Structured split
            for sep in SEPARATORS:
                if sep in text:
                    left, right = text.split(sep, 1)
                    return {
                        "text": left.strip(),
                        "type": "instruction_data",
                        "data_part": right.strip(),
                        "source": "text"
                    }

            # 🔹 Action exists → treat as instruction
            if contains_action(text):
                return {
                    "text": text,
                    "type": "instruction_only",
                    "data_part": None,
                    "source": "text"
                }

            # 🔹 Data only
            return {
                "text": "",
                "type": "data_only",
                "data_part": text,
                "source": "text"
            }

    # =========================
    # 2. AUDIO SECONDARY
    # =========================
    if audio_data:
        first_audio = audio_data[0].get("transcribed_text", "").strip().lower()

        if first_audio:
            if contains_action(first_audio):
                return {
                    "text": first_audio,
                    "type": "instruction_only",
                    "data_part": None,
                    "source": "audio"
                }

    # =========================
    # 3. DEFAULT BUILDER
    # =========================
    instructions = []

    # Audio default
    if audio_data:
        instructions.append("convert audio to text")

    # File default
    for f in files:
        name = f.get("file_name", "").lower()

        if name.endswith((".csv", ".xlsx")):
            instructions.append("analyze file")
        else:
            instructions.append("summarize file")

    # Image default
    if images:
        instructions.append("describe image")

    if not instructions:
        instructions.append("process input")

    return {
        "text": " and ".join(instructions),
        "type": "default",
        "data_part": None,
        "source": "default"
    }