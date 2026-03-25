from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    UPLOAD_DIR: str = "/tmp/uploads"

    ALLOWED_AUDIO_TYPES: List[str] = ["wav", "mp3", "m4a", "webm"]
    ALLOWED_FILE_TYPES: List[str] = ["pdf", "docx", "txt", "csv", "xlsx", "pptx"]
    ALLOWED_IMAGE_TYPES: List[str] = ["jpg", "jpeg", "png", "webp", "bmp"]

settings = Settings()