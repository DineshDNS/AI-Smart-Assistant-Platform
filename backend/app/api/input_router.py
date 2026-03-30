from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional

from app.services.input_handler_service import process_input
from app.services.preprocessing.preprocessing_service import run_preprocessing
from app.services.normalization.normalization_service import run_normalization
from app.services.cache.cache_service import CacheService

# 🔥 NEW IMPORT
from app.memory.memory_manager import MemoryManager


router = APIRouter()

cache_service = CacheService()

# 🔥 Initialize once (important for performance)
memory_manager = MemoryManager()


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
    Input → Preprocessing → Normalization → Cache → Memory → Response
    """

    # Normalize None → []
    audio = audio or []
    file = file or []
    image = image or []

    # =========================
    # STEP 1: INPUT HANDLER
    # =========================
    input_result = process_input(
        text, audio, file, image, user_id, session_id
    )

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

        # Update request_id
        cached_response["request_id"] = normalized_data["request_id"]

        # Mark source
        cached_response["source"] = "cache"

        return cached_response

    # =========================
    # STEP 5: MEMORY LAYER 🔥
    # =========================
    enriched_data = memory_manager.process(normalized_data)

    # =========================
    # (Future) Intelligence Layer
    # =========================
    final_response = enriched_data

    # =========================
    # STEP 6: CACHE STORE
    # =========================
    cache_service.store_cache(
        cache_result["key"],
        final_response
    )

    # =========================
    # STEP 7: MEMORY UPDATE 🔥
    # =========================
    memory_manager.update(
        normalized_data,
        final_response
    )

    return final_response