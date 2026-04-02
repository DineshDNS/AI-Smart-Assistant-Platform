import cv2
import os
from pathlib import Path

# OPTIONAL OCR (enable if installed)
try:
    import pytesseract
    OCR_ENABLED = True
except:
    OCR_ENABLED = False


def process_image(image_path: str) -> dict:

    image_path = os.path.abspath(image_path)

    if not os.path.exists(image_path):
        raise FileNotFoundError("Invalid image path")

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Failed to load image")

    height, width = img.shape[:2]
    channels = img.shape[2] if len(img.shape) == 3 else 1

    # =========================
    # 🔥 BASIC DESCRIPTION (fallback)
    # =========================
    description = f"Image with resolution {width}x{height} and {channels} channels"

    # =========================
    # 🔥 OCR TEXT
    # =========================
    ocr_text = ""
    if OCR_ENABLED:
        try:
            ocr_text = pytesseract.image_to_string(img)
        except:
            ocr_text = ""

    # =========================
    # 🔥 FINAL TEXT (CRITICAL)
    # =========================
    final_text = description
    if ocr_text:
        final_text += f". Detected text: {ocr_text.strip()}"

    return {
        "type": "text",   # 🔥 IMPORTANT → convert to TEXT pipeline
        "content": final_text,
        "metadata": {
            "source": "image",
            "file_path": image_path,
            "width": int(width),
            "height": int(height),
            "channels": int(channels),
            "format": Path(image_path).suffix.replace(".", ""),
            "ocr_enabled": OCR_ENABLED
        }
    }