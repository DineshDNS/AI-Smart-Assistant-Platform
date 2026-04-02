def extract_primary_content(data: list) -> str:
    if not data:
        return ""
    return data[0].get("content", "")


def build_prompt(action: str, tool: str, data: list, memory_context: str = "") -> str:

    content = extract_primary_content(data)

    context_block = f"\nContext:\n{memory_context}\n" if memory_context else ""

    if tool == "explainer":
        if action == "describe":
            return f"{context_block}\nDescribe the image:\n\n{content}"
        return f"{context_block}\nExplain:\n\n{content}"

    if tool == "summarizer":
        return f"{context_block}\nSummarize:\n\n{content}"

    if tool == "converter":
        return f"{context_block}\nConvert:\n\n{content}"

    if tool == "chatbot":
        return f"{context_block}\nUser: {content}\nAssistant:"

    return f"{context_block}\nProcess:\n\n{content}"