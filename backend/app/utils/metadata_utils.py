import mimetypes
import os


def extract_metadata(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    size = os.path.getsize(file_path)
    extension = file_path.split('.')[-1]
    filename = os.path.basename(file_path)

    return {
        "mime": mime_type,
        "size": size,
        "extension": extension,
        "filename": filename
    }