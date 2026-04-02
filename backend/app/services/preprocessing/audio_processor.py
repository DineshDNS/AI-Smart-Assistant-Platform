import whisper
import os
from app.utils.metadata_utils import extract_metadata

_model = None


def get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")
    return _model


def process_audio(audio_path: str) -> dict:
    try:
        absolute_path = os.path.abspath(audio_path)

        if not os.path.exists(absolute_path):
            return {
                "type": "text",
                "content": "",
                "metadata": {
                    "source": "audio",
                    "error": "file_not_found",
                    "file_path": absolute_path
                }
            }

        model = get_model()
        result = model.transcribe(absolute_path)

        metadata = extract_metadata(absolute_path)

        return {
            "type": "text",
            "content": result.get("text", "").strip(),
            "metadata": {
                "source": "audio",
                "file_path": absolute_path,
                "language": result.get("language", "unknown"),
                "confidence": result.get("confidence", None),
                **metadata
            }
        }

    except Exception as e:
        return {
            "type": "text",
            "content": "",
            "metadata": {
                "source": "audio",
                "error": "transcription_failed",
                "message": str(e)
            }
        }