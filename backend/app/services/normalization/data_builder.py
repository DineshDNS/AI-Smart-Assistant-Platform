def build_data(preprocessed_data: dict, instruction: dict):

    processed = preprocessed_data.get("processed_data", {})
    data_items = []

    text_data = processed.get("text")
    audio_data = processed.get("audio_text", [])

    # =========================
    # TEXT
    # =========================
    if text_data:
        original = text_data.get("original", "").strip()

        # 🔥 Conversation case
        if instruction.get("type") == "conversation":
            if instruction.get("data_part"):
                data_items.append({
                    "type": "text",
                    "content": instruction.get("data_part"),
                    "metadata": {"source": "conversation"}
                })

        # 🔹 Instruction + Data (structured split)
        elif instruction.get("type") == "instruction_data":
            if instruction.get("data_part"):
                data_items.append({
                    "type": "text",
                    "content": instruction.get("data_part"),
                    "metadata": {"source": "text"}
                })

        # 🔹 Data only
        elif instruction.get("type") == "data_only":
            if original:
                data_items.append({
                    "type": "text",
                    "content": original,
                    "metadata": {"source": "text"}
                })

    # =========================
    # AUDIO (LIST FORMAT)
    # =========================
    audio_list = []

    for audio in audio_data:
        txt = audio.get("transcribed_text", "").strip()
        if txt:
            audio_list.append({"text": txt})

    if audio_list:
        data_items.append({
            "type": "audio",
            "content": audio_list,
            "metadata": {"count": len(audio_list)}
        })

    # =========================
    # FILES (DEDUP)
    # =========================
    seen = set()

    for f in processed.get("file", []):
        name = f.get("file_name")

        if not name or name in seen:
            continue
        seen.add(name)

        if f.get("category") == "document":
            data_items.append({
                "type": "document",
                "content": f.get("document_text"),
                "metadata": {"file_name": name}
            })

        elif f.get("category") == "tabular":
            data_items.append({
                "type": "tabular",
                "content": f.get("rows"),
                "metadata": {"file_name": name}
            })

    # =========================
    # IMAGE
    # =========================
    for img in processed.get("image", []):
        data_items.append({
            "type": "image",
            "content": img.get("file_path"),
            "metadata": {
                "width": img.get("width"),
                "height": img.get("height"),
                "format": img.get("format")
            }
        })

    return data_items