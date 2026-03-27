import whisper
import os

model = whisper.load_model("base")

audio_path = r"C:\Users\user\Documents\Dinesh_Individual_Projects_Final\Ai-Ml_Projects\AI-Smart-Assistant-Platform\backend\tmp\uploads\e6ef5a96-e7ed-40f9-8c4c-53666a0ab355.mp3"

print("Checking file:", audio_path)
print("Exists:", os.path.exists(audio_path))

result = model.transcribe(audio_path)

print("\nTranscription Result:")
print(result["text"])