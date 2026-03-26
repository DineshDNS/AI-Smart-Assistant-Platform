import re


def extract_instruction(data: dict) -> dict:
    processed = data.get("processed_data", {})

    text_data = processed.get("text")
    audio_data = processed.get("audio_text")
    file_data = processed.get("file")
    image_data = processed.get("image")

    # TEXT PRIORITY
    if text_data:
        cleaned_text = text_data.get("cleaned", "")

        instruction_text, extracted_data = split_text(cleaned_text)

        tokens = [
            t.strip() for t in instruction_text.split()
            if t and t.strip()
        ]

        return {
            "text": instruction_text.strip(),
            "tokens": tokens,
            "_extracted_data": extracted_data
        }

    # AUDIO AS INSTRUCTION
    if audio_data:
        instruction_text = audio_data.get("transcribed_text", "").strip()

        tokens = [
            t.strip() for t in instruction_text.split()
            if t and t.strip()
        ]

        return {
            "text": instruction_text,
            "tokens": tokens,
            "_extracted_data": None
        }

    # IMAGE ONLY DEFAULT
    if image_data and not file_data:
        return {
            "text": "describe the image",
            "tokens": ["describe", "image"],
            "_extracted_data": None
        }

    # FILE ONLY DEFAULT
    if file_data:
        first_file = file_data[0] if isinstance(file_data, list) else file_data

        if first_file.get("category") == "document":
            return {
                "text": "summarize the file",
                "tokens": ["summarize", "file"],
                "_extracted_data": None
            }

        elif first_file.get("category") == "tabular":
            return {
                "text": "analyze the data",
                "tokens": ["analyze", "data"],
                "_extracted_data": None
            }

    return {
        "text": "",
        "tokens": [],
        "_extracted_data": None
    }


def split_text(text: str):
    text = text.strip()

    # SYMBOL-BASED SPLIT
    separators = [":", "-", "→", "=>"]

    for sep in separators:
        if sep in text:
            parts = text.split(sep, 1)
            instruction = parts[0]
            data = parts[1]
            return instruction.strip(), clean_data_text(data)

    # NLP-CLEANED PATTERN SUPPORT
    pattern = r"^(summarize|explain|analyze|describe|predict|detect)\s+(follow|following|below|this|given)\s+(.*)"

    match = re.match(pattern, text, re.IGNORECASE)

    if match:
        instruction = match.group(1)
        data = match.group(3)
        return instruction.strip(), clean_data_text(data)

    # NEWLINE SPLIT
    if "\n" in text:
        parts = text.split("\n", 1)
        return parts[0].strip(), clean_data_text(parts[1])

    return text, None


def clean_data_text(data: str):
    """
    Cleans extracted data:
    - Keeps only meaningful content
    - Removes extra instructions
    - Works even without punctuation
    """

    data = data.strip()

    # 1. Try sentence split
    sentences = re.split(r'(?<=[.!?])\s+', data)

    if sentences and len(sentences[0].split()) > 3:
        data = sentences[0].strip()

    # 2. Stop at instruction verbs
    stop_words = [
        "summarize", "explain", "analyze",
        "describe", "predict", "detect", "verify"
    ]

    words = data.split()

    cleaned_words = []
    for word in words:
        if word.lower() in stop_words and len(cleaned_words) > 3:
            break
        cleaned_words.append(word)

    return " ".join(cleaned_words).strip()