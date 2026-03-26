def build_data(preprocessed_data: dict, instruction: dict) -> list:
    processed = preprocessed_data.get("processed_data", {})
    data_items = []

    extracted_text_data = instruction.get("_extracted_data")

    # Text data from split
    if extracted_text_data:
        cleaned_data = extracted_text_data.strip()

        if cleaned_data:
            data_items.append({
                "type": "text",
                "content": cleaned_data,
                "metadata": {
                    "length": len(cleaned_data)
                }
            })

    # Audio as data only if text exists
    audio_data = processed.get("audio_text")
    text_data = processed.get("text")

    if audio_data and text_data:
        content = audio_data.get("transcribed_text", "").strip()

        if content:
            data_items.append({
                "type": "audio",
                "content": content,
                "metadata": {}
            })

    # File handling
    files = processed.get("file", [])
    for f in files:
        if f.get("category") == "document":
            data_items.append({
                "type": "document",
                "content": f.get("document_text"),
                "metadata": {
                    "file_name": f.get("file_name")
                }
            })

        elif f.get("category") == "tabular":
            data_items.append({
                "type": "tabular",
                "content": f.get("rows"),
                "metadata": {
                    "file_name": f.get("file_name")
                }
            })

    # Image handling
    if processed.get("image"):
        img = processed["image"]
        data_items.append({
            "type": "image",
            "content": img.get("file_path"),
            "metadata": {
                "width": img.get("width"),
                "height": img.get("height"),
                "channels": img.get("channels"),
                "format": img.get("format")
            }
        })

    return data_items