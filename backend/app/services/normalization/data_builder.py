def safe_extract_content(content):

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


def build_data(preprocessed_data: dict, instruction: dict):

    processed = preprocessed_data.get("processed_data", {})
    raw_items = processed.get("data", [])

    data_items = []

    for item in raw_items:
        if not item:
            continue

        raw_content = item.get("content", "")
        metadata = item.get("metadata", {})
        source = metadata.get("source", "unknown")

        content = safe_extract_content(raw_content).strip()

        if not content and not metadata.get("error"):
            continue

        # =========================
        # 🔥 FILE PRIORITY (FIX)
        # =========================
        if source == "file":
            data_items.append({
                "type": "text",
                "content": content,
                "metadata": metadata
            })
            continue

        # =========================
        # 🔥 REMOVE COMMAND DUPLICATION
        # =========================
        if source == "text" and instruction.get("type") == "instruction_only":
            continue

        # =========================
        # DEFAULT (ALL → TEXT)
        # =========================
        data_items.append({
            "type": "text",
            "content": content,
            "metadata": metadata
        })

    return data_items