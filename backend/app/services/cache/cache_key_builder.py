import hashlib
import json


def normalize_for_cache(data_items):
    """
    Normalize data for stable cache key
    """

    normalized = []

    for item in data_items:

        clean = {"type": item.get("type")}

        # TEXT
        if item["type"] == "text":
            clean["content"] = item.get("content")

        # IMAGE
        elif item["type"] == "image":
            meta = item.get("metadata", {})
            clean["content"] = {
                "width": meta.get("width"),
                "height": meta.get("height"),
                "format": meta.get("format")
            }

        # TABULAR
        elif item["type"] == "tabular":
            content = item.get("content", {})
            clean["content"] = {
                "columns": content.get("columns"),
                "shape": content.get("shape")
            }

        # DOCUMENT (OPTIONAL ADD)
        elif item["type"] == "document":
            clean["content"] = {
                "length": len(item.get("content", ""))
            }

        normalized.append(clean)

    # 🔥 SORT FOR CONSISTENCY
    return sorted(normalized, key=lambda x: json.dumps(x, sort_keys=True))


# ✅ REQUIRED FUNCTION (MISSING BEFORE)
def build_cache_key(normalized_data: dict, user_id: str = None):
    """
    Build stable cache key
    """

    key_payload = {
        "instruction": normalized_data.get("instruction", {}),
        "data": normalize_for_cache(normalized_data.get("data", []))
    }

    if user_id:
        key_payload["user_id"] = user_id

    key_string = json.dumps(key_payload, sort_keys=True)

    return "cache:" + hashlib.sha256(key_string.encode()).hexdigest()