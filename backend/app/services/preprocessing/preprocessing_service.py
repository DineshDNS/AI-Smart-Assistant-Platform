from app.services.preprocessing.text_processor import process_text
from app.services.preprocessing.audio_processor import process_audio
from app.services.preprocessing.file_processor import process_files
from app.services.preprocessing.image_processor import process_image


def run_preprocessing(input_data: dict) -> dict:
    processed_data = {}
    summary = {}
    errors = []

    data = input_data.get("data", {})
    flags = input_data.get("processing_flags", {})

    # TEXT
    try:
        if data.get("text") and flags.get("needs_cleaning"):
            processed_data["text"] = process_text(data["text"])
            summary["text_cleaned"] = True
    except Exception as e:
        errors.append({"module": "text", "message": str(e)})

    # AUDIO
    try:
        if data.get("audio") and flags.get("needs_transcription"):
            processed_data["audio_text"] = process_audio(data["audio"])
            summary["audio_transcribed"] = True
    except Exception as e:
        errors.append({"module": "audio", "message": str(e)})

    # FILE
    try:
        if data.get("file") and flags.get("needs_file_processing", True):
            processed_data["file"] = process_files(data["file"])
            summary["file_processed"] = True
    except Exception as e:
        errors.append({"module": "file", "message": str(e)})

    # IMAGE
    try:
        if data.get("image") and flags.get("needs_image_processing", True):
            processed_data["image"] = process_image(data["image"])
            summary["image_processed"] = True
    except Exception as e:
        errors.append({"module": "image", "message": str(e)})

    return {
        "request_id": input_data["request_id"],
        "user_id": input_data["user_id"],
        "status": "processed",
        "processed_data": processed_data,
        "processing_summary": summary,
        "errors": errors
    }