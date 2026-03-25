import whisper
import os

model = whisper.load_model("base")


def process_audio(audio_path: str) -> dict:
    # ✅ Convert to absolute path
    absolute_path = os.path.abspath(audio_path)

    print("Audio path:", absolute_path)
    print("File exists:", os.path.exists(absolute_path))

    if not os.path.exists(absolute_path):
        raise FileNotFoundError(f"Audio file not found: {absolute_path}")

    result = model.transcribe(absolute_path)

    return {
        "original_audio_path": absolute_path,
        "transcribed_text": result["text"]
    }