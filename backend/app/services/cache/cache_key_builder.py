
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

        # DOCUMENT
        elif item["type"] == "document":
            content = item.get("content", "")
            clean["content"] = {
                "length": len(content)
            }

        normalized.append(clean)

    # 🔥 SORT FOR CONSISTENCY
    return sorted(normalized, key=lambda x: json.dumps(x, sort_keys=True))


def build_cache_key(
    normalized_data: dict,
    intent_data: dict = None,
    user_id: str = None
):
    """
    Build semantic + stable cache key
    """

    # =========================
    # 🔹 BASE PAYLOAD
    # =========================
    key_payload = {
        "modalities": normalized_data.get("summary", {}).get("modalities", []),
        "data": normalize_for_cache(normalized_data.get("data", [])),
    }

    # =========================
    # 🔥 USE ACTIONS (MOST IMPORTANT FIX)
    # =========================
    if intent_data and intent_data.get("actions"):
        key_payload["actions"] = [a["name"] for a in intent_data["actions"]]
    else:
        # fallback (only if intent not available)
        key_payload["instruction"] = normalized_data.get("instruction", {}).get("text", "")

    # =========================
    # 🔹 USER-SPECIFIC CACHE (OPTIONAL)
    # =========================
    if user_id:
        key_payload["user_id"] = user_id

    # =========================
    # 🔹 FINAL HASH
    # =========================
    key_string = json.dumps(key_payload, sort_keys=True)

    return "cache:" + hashlib.sha256(key_string.encode()).hexdigest()

