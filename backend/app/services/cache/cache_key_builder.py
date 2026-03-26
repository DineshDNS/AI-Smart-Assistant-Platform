import hashlib
import json


def normalize_for_cache(data_items):
    """
    Remove unstable fields like file paths, UUID names
    Keep only meaningful content
    """
    normalized = []

    for item in data_items:
        clean_item = {
            "type": item.get("type")
        }

        # TEXT
        if item["type"] == "text":
            clean_item["content"] = item.get("content")

        # TABULAR
        elif item["type"] == "tabular":
            content = item.get("content", {})
            clean_item["content"] = {
                "columns": content.get("columns"),
                "shape": content.get("shape")
            }

        # IMAGE
        elif item["type"] == "image":
            metadata = item.get("metadata", {})
            clean_item["content"] = {
                "width": metadata.get("width"),
                "height": metadata.get("height"),
                "format": metadata.get("format")
            }

        normalized.append(clean_item)

    return normalized


def build_cache_key(normalized_data: dict, user_id: str = None) -> str:
    key_payload = {
        "instruction": normalized_data.get("instruction", {}),
        "data": normalize_for_cache(normalized_data.get("data", []))
    }

    if user_id:
        key_payload["user_id"] = user_id

    key_string = json.dumps(key_payload, sort_keys=True)

    return "cache:" + hashlib.sha256(key_string.encode()).hexdigest()