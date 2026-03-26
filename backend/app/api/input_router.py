from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional

from app.services.input_handler_service import process_input
from app.services.preprocessing.preprocessing_service import run_preprocessing
from app.services.normalization.normalization_service import run_normalization  # ✅ NEW

router = APIRouter()


@router.post("/input")
async def handle_input(
    text: Optional[str] = Form(None),
    user_id: str = Form(...),
    audio: Optional[UploadFile] = File(None),
    file: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None)
):
    """
    FINAL PIPELINE:
    Input Handler → Preprocessing → Normalization → Response
    """

    # Step 1: Input Handling
    input_result = process_input(text, audio, file, image, user_id)

    if not input_result.get("valid"):
        return input_result

    # Step 2: Preprocessing
    preprocessed_data = run_preprocessing(input_result)

    # Step 3: Normalization
    normalized_data = run_normalization(preprocessed_data)

    return normalized_data