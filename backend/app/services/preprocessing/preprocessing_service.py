from app.services.preprocessing.text_processor import process_text
from app.services.preprocessing.audio_processor import process_audio
from app.services.preprocessing.file_processor import process_files
from app.services.preprocessing.image_processor import process_image


def run_preprocessing(input_data: dict):

    processed = {}
    errors = []

    data = input_data["data"]

    # TEXT
    if data.get("text"):
        processed["text"] = process_text(data["text"])

    # AUDIO (MULTI)
    if data.get("audio"):
        processed["audio_text"] = []
        for a in data["audio"]:
            try:
                processed["audio_text"].append(process_audio(a))
            except Exception as e:
                errors.append({"audio": str(e)})

    # FILE
    if data.get("file"):
        processed["file"] = process_files(data["file"])

    # IMAGE (MULTI)
    if data.get("image"):
        processed["image"] = []
        for img in data["image"]:
            try:
                processed["image"].append(process_image(img))
            except Exception as e:
                errors.append({"image": str(e)})

    return {
        "request_id": input_data["request_id"],
        "user_id": input_data["user_id"],
        "status": "processed",
        "processed_data": processed,
        "errors": errors,
    }