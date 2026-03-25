import cv2
import os
from pathlib import Path


def process_image(image_path: str) -> dict:
    # Absolute path
    image_path = os.path.abspath(image_path)

    if not os.path.exists(image_path):
        raise FileNotFoundError("Invalid image path")

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Failed to load image")

    height, width = img.shape[:2]
    channels = img.shape[2] if len(img.shape) == 3 else 1

    return {
        "file_path": image_path,
        "width": int(width),
        "height": int(height),
        "channels": int(channels),
        "format": Path(image_path).suffix.replace(".", ""),
        "ready_for_detection": True   # important flag
    }