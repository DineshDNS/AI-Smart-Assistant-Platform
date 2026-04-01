def select_tool(action: str, input_type: str) -> str:

    action = (action or "").lower()
    input_type = (input_type or "").lower()

    # =========================
    # IMAGE → ALWAYS VISION
    # =========================
    if input_type == "image":
        return "vision"

    # =========================
    # TABULAR
    # =========================
    if input_type == "tabular":
        return "analyzer"

    # =========================
    # DOCUMENT
    # =========================
    if input_type == "document":
        if action in ["summarize", "explain"]:
            return "summarizer"
        if action == "translate":
            return "translator"
        return "analyzer"

    # =========================
    # AUDIO
    # =========================
    if input_type == "audio":
        if action == "transcribe":
            return "converter"
        return "summarizer"

    # =========================
    # TEXT
    # =========================
    if input_type == "text":

        action_tool_map = {
            "summarize": "summarizer",
            "translate": "translator",
            "explain": "explainer",   # 🔥 CRITICAL FIX
            "generate": "generator",
            "analyze": "analyzer",
            "convert": "converter",
            "extract": "analyzer",
            "conversation": "chatbot",
        }

        return action_tool_map.get(action, "chatbot")

    # =========================
    # FALLBACK (SAFE)
    # =========================
    return "chatbot"