def validate_file_type(filename: str, allowed_types: list):
    if not filename:
        return False, "No file provided"

    ext = filename.split('.')[-1].lower()

    if ext not in allowed_types:
        return False, f"Unsupported format: {ext}"

    return True, ext