def build_summary(data: list) -> dict:
    types = list(set([item["type"] for item in data]))

    return {
        "total_items": len(data),
        "modalities": types
    }