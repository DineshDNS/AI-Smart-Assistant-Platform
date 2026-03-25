from app.utils.id_utils import generate_request_id, get_timestamp
from app.utils.file_utils import save_file
from app.utils.metadata_utils import extract_metadata
from app.utils.validation_utils import validate_file_type
from app.core.config import settings


def process_input(text, audio, file, image, user_id):
    request_id = generate_request_id()
    timestamp = get_timestamp()

    input_types = []
    data = {"text": None, "audio": None, "file": None, "image": None}
    metadata = {
        "size": {},
        "mime_types": {},
        "source": {}
    }
    errors = []

    # TEXT
    if text and text.strip():
        input_types.append("text")
        data["text"] = text
        metadata["source"]["text"] = "user"

    # AUDIO
    if audio:
        is_valid, result = validate_file_type(audio.filename, settings.ALLOWED_AUDIO_TYPES)

        if not is_valid:
            errors.append({
                "type": "validation_error",
                "message": f"Audio error: {result}"
            })
        else:
            input_types.append("audio")
            audio_path = save_file(audio)
            data["audio"] = audio_path

            meta = extract_metadata(audio_path)
            metadata["audio_format"] = result
            metadata["audio_name"] = audio.filename
            metadata["size"]["audio"] = meta["size"]
            metadata["mime_types"]["audio"] = meta["mime"] or "unknown"
            metadata["source"]["audio"] = "upload"

    # FILE
    if file:
        is_valid, result = validate_file_type(file.filename, settings.ALLOWED_FILE_TYPES)

        if not is_valid:
            errors.append({
                "type": "validation_error",
                "message": f"File error: {result}"
            })
        else:
            input_types.append("file")
            file_path = save_file(file)
            data["file"] = file_path

            meta = extract_metadata(file_path)
            metadata["file_type"] = result
            metadata["file_name"] = file.filename
            metadata["size"]["file"] = meta["size"]
            metadata["mime_types"]["file"] = meta["mime"] or "unknown"
            metadata["source"]["file"] = "upload"

    # IMAGE
    if image:
        is_valid, result = validate_file_type(image.filename, settings.ALLOWED_IMAGE_TYPES)

        if not is_valid:
            errors.append({
                "type": "validation_error",
                "message": f"Image error: {result}"
            })
        else:
            input_types.append("image")
            image_path = save_file(image)
            data["image"] = image_path

            meta = extract_metadata(image_path)
            metadata["image_format"] = result
            metadata["image_name"] = image.filename
            metadata["size"]["image"] = meta["size"]
            metadata["mime_types"]["image"] = meta["mime"] or "unknown"
            metadata["source"]["image"] = "upload"

    # FINAL VALIDATION (STRICT MODE)
    valid = len(errors) == 0 and len(input_types) > 0

    # 🔹 PROCESSING FLAGS
    processing_flags = {
        "needs_transcription": "audio" in input_types,
        "needs_ocr": "image" in input_types,
        "needs_cleaning": "text" in input_types
    }

    return {
        "request_id": request_id,
        "timestamp": timestamp,
        "user_id": user_id,
        "status": "success" if valid else "error",
        "valid": valid,
        "input_types": input_types if valid else [],
        "data": data,
        "metadata": metadata,
        "processing_flags": processing_flags,
        "errors": errors
    }