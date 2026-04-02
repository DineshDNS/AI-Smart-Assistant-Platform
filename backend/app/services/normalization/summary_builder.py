def build_summary(data: list) -> dict:

    modalities = set()

    has_audio = False
    has_text = False
    has_file = False
    has_image = False

    for item in data:
        source = item.get("metadata", {}).get("source")

        if source == "audio":
            has_audio = True
            modalities.add("audio")

        elif source == "text":
            has_text = True
            modalities.add("text")

        elif source == "file":
            has_file = True
            modalities.add("file")

        elif source == "image":
            has_image = True
            modalities.add("image")

    return {
        "total_items": len(data),
        "modalities": list(modalities),
        "has_audio": has_audio,
        "has_text": has_text,
        "has_file": has_file,
        "has_image": has_image
    }