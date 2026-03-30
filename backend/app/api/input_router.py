from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional

from app.services.input_handler_service import process_input
from app.services.preprocessing.preprocessing_service import run_preprocessing
from app.services.normalization.normalization_service import run_normalization
from app.services.cache.cache_service import CacheService

router = APIRouter()
cache_service = CacheService()


@router.post("/input")
async def handle_input(
    text: Optional[str] = Form(None),
    user_id: str = Form(...),
    session_id: str = Form(...),

    audio: Optional[List[UploadFile]] = File(None),
    file: Optional[List[UploadFile]] = File(None),
    image: Optional[List[UploadFile]] = File(None),
):
    """
    PIPELINE:
    Input → Preprocessing → Normalization → Cache → Response
    """

    audio = audio or []
    file = file or []
    image = image or []

    # =========================
    # STEP 1: INPUT HANDLING
    # =========================
    input_result = process_input(text, audio, file, image, user_id, session_id)  # 🔥 UPDATED

    if not input_result.get("valid"):
        return input_result

    # =========================
    # STEP 2: PREPROCESSING
    # =========================
    preprocessed_data = run_preprocessing(input_result)

    # =========================
    # STEP 3: NORMALIZATION
    # =========================
    normalized_data = run_normalization(preprocessed_data)

    if normalized_data.get("status") == "failed":
        return normalized_data

    # =========================
    # STEP 4: CACHE CHECK
    # =========================
    cache_result = cache_service.check_cache(
        normalized_data,
        user_id=normalized_data.get("user_id")
    )

    # =========================
    # CACHE HIT
    # =========================
    if cache_result["cache_hit"]:
        cached_response = cache_result["data"]

        cached_response["request_id"] = normalized_data["request_id"]
        cached_response["source"] = "cache"

        return cached_response

    # =========================
    # CACHE MISS
    # =========================
    final_response = normalized_data

    # =========================
    # STORE CACHE
    # =========================
    cache_service.store_cache(
        cache_result["key"],
        final_response
    )

    return final_response