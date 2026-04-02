def select_tool(action: str, input_type: str) -> str:

    action = (action or "").lower()

    return {
        "summarize": "summarizer",
        "translate": "translator",
        "explain": "explainer",
        "generate": "generator",
        "analyze": "analyzer",
        "convert": "converter",
        "extract": "analyzer",
        "detect": "analyzer",   
        "conversation": "chatbot",
        "describe": "explainer"
    }.get(action, "chatbot")