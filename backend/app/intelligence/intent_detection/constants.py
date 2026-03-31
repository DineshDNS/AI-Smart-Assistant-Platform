ACTION_GROUPS = {
    "summarize": ["summarize", "summary", "brief", "shorten", "condense"],
    "analyze": ["analyze", "analysis", "examine", "evaluate", "inspect"],
    "translate": ["translate", "interpret"],
    "generate": ["generate", "create", "write", "produce", "recommend"],
    "explain": ["explain", "clarify", "elaborate", "teach"],
    "describe": ["describe", "detail", "outline"],
    "classify": ["classify", "categorize", "group"],
    "extract": ["extract", "get", "retrieve", "list"],
    "convert": ["convert", "transform", "change", "rewrite", "format"],
    "predict": ["predict", "forecast", "estimate"],
    "compare": ["compare", "contrast"],
    "detect": ["detect", "identify", "find"],
    "transcribe": ["transcribe", "listen"]
}

PHRASE_MAP = {
    "short version": "summarize",
    "key points": "extract",
    "main points": "extract",
    "in simple terms": "explain",
    "step by step": "explain",
    "what is happening": "describe",
    "convert into": "convert",
    "turn into": "convert",
    "future trend": "predict",
    "what will happen": "predict",
    "difference between": "compare"
}

MULTI_ACTION_SEPARATORS = [
    "and", ",", "+", "&", "then", "also",
    "as well as", "along with", "followed by",
    "after that", "or"
]