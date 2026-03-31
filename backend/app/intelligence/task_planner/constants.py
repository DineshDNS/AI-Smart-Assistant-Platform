
# =========================
# 🧠 ACTION → TARGET MAP
# =========================

ACTION_TARGET_MAP = {

    # 🟢 TEXT / DOCUMENT OPERATIONS
    "summarize": ["document", "text", "pdf", "article", "report"],
    "explain": ["text", "document", "audio", "code"],
    "describe": ["image", "video", "object"],
    "analyze": ["text", "document", "tabular", "csv", "json"],
    "extract": ["text", "document", "image", "pdf"],
    "classify": ["text", "image", "document"],
    "translate": ["text", "document", "audio"],
    "rewrite": ["text", "document"],
    "simplify": ["text", "document"],
    "expand": ["text", "document"],
    "correct": ["text", "document"],

    # 🔵 MEDIA OPERATIONS
    "transcribe": ["audio", "video"],
    "convert": ["text", "audio", "image", "document", "video"],
    "generate": ["text", "image", "audio"],
    "create": ["text", "image", "audio"],
    "edit": ["image", "text", "document"],
    "enhance": ["image", "audio"],
    "compress": ["image", "video", "document"],

    # 🟡 DATA / FILE OPERATIONS
    "filter": ["tabular", "json", "csv"],
    "sort": ["tabular", "json"],
    "aggregate": ["tabular"],
    "visualize": ["tabular", "csv"],
    "predict": ["tabular", "time_series"],

    # 🔴 SPECIAL OPERATIONS
    "search": ["text", "web"],
    "compare": ["text", "document"],
    "detect": ["image", "audio", "text"],
}


# =========================
# 🔥 TRANSFORMATION KEYWORDS
# =========================

TRANSFORMATION_KEYWORDS = {

    # 🎧 AUDIO OUTPUT
    "audio": [
        "to audio", "into audio",
        "to speech", "into speech",
        "to voice", "into voice",
        "to mp3", "to wav",
        "text to audio", "text to speech",
        "read aloud", "speak this",
        "convert to audio", "make it audio"
    ],

    # 📝 TEXT OUTPUT
    "text": [
        "to text", "into text",
        "to plain text",
        "audio to text", "speech to text",
        "convert to text",
        "write it", "give text",
        "transcribe", "extract text",
        "convert into words"
    ],

    # 🖼 IMAGE OUTPUT
    "image": [
        "to image", "into image",
        "to picture", "into picture",
        "generate image", "create image",
        "text to image",
        "make it visual", "draw this",
        "convert to png", "convert to jpg"
    ],

    # 📄 DOCUMENT OUTPUT
    "document": [
        "to pdf", "into pdf",
        "to doc", "to docx",
        "to document", "into document",
        "convert to file",
        "save as pdf",
        "export as document"
    ],

    # 🎥 VIDEO OUTPUT
    "video": [
        "to video", "into video",
        "generate video",
        "convert to mp4",
        "make video"
    ],

    # 📊 STRUCTURED DATA OUTPUT
    "tabular": [
        "to table", "into table",
        "to csv", "to excel",
        "convert to spreadsheet",
        "tabular format"
    ]
}
