import os
from app.services.preprocessing.loaders.pdf_loader import extract_pdf
from app.services.preprocessing.loaders.docx_loader import extract_docx
from app.services.preprocessing.loaders.tabular_loader import load_tabular


def convert_numpy(obj):
    """Convert numpy/pandas types to Python native"""
    if hasattr(obj, "item"):
        return obj.item()
    return obj


def make_json_safe(data):
    """Recursively convert all values to JSON-safe types"""
    if isinstance(data, dict):
        return {k: make_json_safe(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [make_json_safe(v) for v in data]
    else:
        return convert_numpy(data)


def process_files(file_paths):
    if not isinstance(file_paths, list):
        file_paths = [file_paths]

    results = []

    for path in file_paths:
        ext = path.split(".")[-1].lower()
        file_name = os.path.basename(path)

        # DOCUMENT FILES
        if ext in ["pdf", "docx", "txt"]:
            text = handle_document(path, ext)

            results.append({
                "file_name": file_name,
                "category": "document",
                "document_text": text[:3000]  # 🔥 limit for safety
            })

        # TABULAR FILES
        elif ext in ["csv", "xlsx"]:
            tabular_data = load_tabular(path)

            # FIX: convert to JSON-safe
            safe_data = make_json_safe(tabular_data)

            results.append({
                "file_name": file_name,
                "category": "tabular",
                "rows": safe_data[:50] if isinstance(safe_data, list) else safe_data,
                "note": "Showing limited rows (max 50)"
            })

        else:
            results.append({
                "file_name": file_name,
                "category": "unknown",
                "message": f"Unsupported file type: {ext}"
            })

    return results


def handle_document(path, ext):
    if ext == "pdf":
        return extract_pdf(path)
    elif ext == "docx":
        return extract_docx(path)
    elif ext == "txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()