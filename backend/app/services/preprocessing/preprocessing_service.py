from app.services.preprocessing.text_processor import process_text
from app.services.preprocessing.audio_processor import process_audio
from app.services.preprocessing.file_processor import process_files
from app.services.preprocessing.image_processor import process_image


def run_preprocessing(input_data: dict):

    processed = {"data": []}
    errors = []
    data = input_data["data"]

    # =========================
    # TEXT
    # =========================
    if data.get("text"):
        try:
            text_result = process_text(data["text"])

            processed["data"].append({
                "type": "text",
                "content": text_result,
                "metadata": {"source": "text"}
            })
        except Exception as e:
            errors.append({"text": str(e)})

    # =========================
    # AUDIO
    # =========================
    if data.get("audio"):
        for a in data["audio"]:
            try:
                result = process_audio(a)
                processed["data"].append(result)
            except Exception as e:
                errors.append({"audio": str(e)})

    # =========================
    # FILE (🔥 FIXED STRUCTURE)
    # =========================
    if data.get("file"):
        try:
            file_results = process_files(data["file"])

            if isinstance(file_results, list):
                processed["data"].extend(file_results)
            else:
                processed["data"].append(file_results)

        except Exception as e:
            errors.append({"file": str(e)})

    # =========================
    # IMAGE
    # =========================
    if data.get("image"):
        for img in data["image"]:
            try:
                result = process_image(img)
                processed["data"].append(result)
            except Exception as e:
                errors.append({"image": str(e)})

    return {
        "request_id": input_data["request_id"],
        "user_id": input_data["user_id"],
        "session_id": input_data["session_id"],
        "status": "processed",
        "processed_data": processed,
        "errors": errors,
    }