import os
import shutil
import uuid
from pathlib import Path
from app.core.config import settings


def save_file(upload_file):
    # Ensure upload directory exists
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Extract extension
    file_ext = Path(upload_file.filename).suffix

    # Unique filename
    unique_name = f"{uuid.uuid4()}{file_ext}"

    file_path = upload_dir / unique_name

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    print("Saved file at:", file_path.resolve())

    # Return ABSOLUTE path (IMPORTANT FIX)
    return str(file_path.resolve())