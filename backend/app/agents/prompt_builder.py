def extract_primary_content(data: list) -> str:
    if not data:
        return ""

    content = data[0].get("content", "")

    if isinstance(content, list):
        content = " ".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        )

    return content or ""


def build_prompt(action: str, tool: str, data: list, memory_context: str = "") -> str:

    content = extract_primary_content(data)

    if not content:
        content = memory_context or ""

    if tool == "chatbot":
        return f"{memory_context}\nUser: {content}\nAssistant:"  # 🔥 FIX

    if tool == "explainer":
        return f"Explain in simple terms:\n\n{content}"

    if tool == "summarizer":
        return f"Summarize clearly:\n\n{content}"

    if tool == "translator":
        return f"Translate the following:\n\n{content}"

    if tool == "generator":
        return f"Generate content based on:\n\n{content}"

    if tool == "analyzer":
        return f"Analyze the following:\n\n{content}"

    if tool == "converter":
        return f"Convert the following content:\n\n{content}"

    if tool == "vision":
        if action == "describe":
            return "Describe the image in detail."
        if action == "extract":
            return "Extract all readable text from the image."
        if action == "detect":
            return "Detect all objects in the image."
        return "Analyze the image."

    return f"Process the input:\n\n{content}"