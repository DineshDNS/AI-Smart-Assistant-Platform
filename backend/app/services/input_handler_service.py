from typing import List, Optional
from app.utils.id_utils import generate_request_id, get_timestamp
from app.utils.file_utils import save_file
from app.utils.metadata_utils import extract_metadata
from app.utils.validation_utils import validate_file_type
from app.core.config import settings


def _ensure_list(x):
    if x is None:
        return []
    return x if isinstance(x, list) else [x]


def process_input(text, audio, file, image, user_id, session_id):

    request_id = generate_request_id()
    timestamp = get_timestamp()

    audio_list = _ensure_list(audio)
    file_list = _ensure_list(file)
    image_list = _ensure_list(image)

    input_types = []
    data = {"text": None, "audio": [], "file": [], "image": []}
    metadata = {"size": {}, "mime_types": {}, "source": {}}
    errors = []

    # =========================
    # TEXT
    # =========================
    if text and text.strip():
        input_types.append("text")
        data["text"] = text.strip()
        metadata["source"]["text"] = "user"

    # =========================
    # AUDIO
    # =========================
    for a in audio_list:
        if not a:
            continue

        valid, ext = validate_file_type(a.filename, settings.ALLOWED_AUDIO_TYPES)
        if not valid:
            errors.append({"type": "audio", "message": ext})
            continue

        path = save_file(a)
        data["audio"].append(path)

    if data["audio"]:
        input_types.append("audio")

    # =========================
    # FILE
    # =========================
    for f in file_list:
        if not f:
            continue

        valid, ext = validate_file_type(f.filename, settings.ALLOWED_FILE_TYPES)
        if not valid:
            errors.append({"type": "file", "message": ext})
            continue

        path = save_file(f)
        data["file"].append(path)

    if data["file"]:
        input_types.append("file")

    # =========================
    # IMAGE
    # =========================
    for i in image_list:
        if not i:
            continue

        valid, ext = validate_file_type(i.filename, settings.ALLOWED_IMAGE_TYPES)
        if not valid:
            errors.append({"type": "image", "message": ext})
            continue

        path = save_file(i)
        data["image"].append(path)

    if data["image"]:
        input_types.append("image")

    # =========================
    # ✅ FIXED VALIDATION LOGIC
    # =========================
    if not input_types:
        errors.append({
            "type": "input",
            "message": "At least one valid input required"
        })
        valid = False
    else:
        # ✅ allow partial success
        valid = True

    # =========================
    # FLAGS
    # =========================
    processing_flags = {
        "needs_transcription": bool(data["audio"]),
        "needs_cleaning": bool(data["text"]),
        "needs_file_processing": bool(data["file"]),
        "needs_image_processing": bool(data["image"]),
    }

    return {
        "request_id": request_id,
        "timestamp": timestamp,
        "user_id": user_id,
        "session_id": session_id,
        "status": "success" if valid else "error",
        "valid": valid,
        "input_types": input_types,
        "data": data,
        "metadata": metadata,
        "processing_flags": processing_flags,
        "errors": errors,
    }