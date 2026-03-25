from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    # Save uploads inside project
    UPLOAD_DIR: str = str(BASE_DIR / "tmp" / "uploads")

    ALLOWED_AUDIO_TYPES: List[str] = ["wav", "mp3", "m4a", "webm"]
    ALLOWED_FILE_TYPES: List[str] = ["pdf", "docx", "txt", "csv", "xlsx", "pptx"]
    ALLOWED_IMAGE_TYPES: List[str] = ["jpg", "jpeg", "png", "webp", "bmp"]


settings = Settings()