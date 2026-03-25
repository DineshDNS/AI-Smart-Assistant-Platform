import os
import shutil
from pathlib import Path
from app.core.config import settings

def save_file(upload_file):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    file_path = Path(settings.UPLOAD_DIR) / upload_file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    # FIX: POSIX path
    return file_path.as_posix()