import os
from app.services.preprocessing.loaders.pdf_loader import extract_pdf
from app.services.preprocessing.loaders.docx_loader import extract_docx
from app.services.preprocessing.loaders.tabular_loader import load_tabular


def convert_numpy(obj):
    if hasattr(obj, "item"):
        return obj.item()
    return obj


def make_json_safe(data):
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

        try:
            absolute_path = os.path.abspath(path)

            if not os.path.exists(absolute_path):
                raise FileNotFoundError(f"File not found: {absolute_path}")

            ext = path.split(".")[-1].lower()
            file_name = os.path.basename(path)

            # =========================
            # 📄 DOCUMENT FILES → TEXT
            # =========================
            if ext in ["pdf", "docx", "txt"]:
                text = handle_document(absolute_path, ext)

                results.append({
                    "type": "text",
                    "content": text[:3000],  # safety limit
                    "metadata": {
                        "source": "file",
                        "file_path": absolute_path,
                        "file_name": file_name,
                        "file_type": "document"
                    }
                })

            # =========================
            # 📊 TABULAR FILES
            # =========================
            elif ext in ["csv", "xlsx"]:
                tabular_data = load_tabular(absolute_path)

                safe_data = make_json_safe(tabular_data)

                results.append({
                    "type": "tabular",
                    "content": safe_data[:50] if isinstance(safe_data, list) else safe_data,
                    "metadata": {
                        "source": "file",
                        "file_path": absolute_path,
                        "file_name": file_name,
                        "file_type": "tabular",
                        "note": "Showing limited rows (max 50)"
                    }
                })

            # =========================
            # ❌ UNKNOWN FILE
            # =========================
            else:
                results.append({
                    "type": "error",
                    "content": "",
                    "metadata": {
                        "source": "file",
                        "file_path": absolute_path,
                        "file_name": file_name,
                        "error": f"Unsupported file type: {ext}"
                    }
                })

        except Exception as e:
            results.append({
                "type": "error",
                "content": "",
                "metadata": {
                    "source": "file",
                    "file_path": path,
                    "error": str(e)
                }
            })

    return results


def handle_document(path, ext):
    if ext == "pdf":
        return extract_pdf(path)

    elif ext == "docx":
        return extract_docx(path)

    elif ext == "txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    return ""