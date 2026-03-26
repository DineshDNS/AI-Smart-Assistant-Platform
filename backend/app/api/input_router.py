from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional

from app.services.input_handler_service import process_input
from app.services.preprocessing.preprocessing_service import run_preprocessing
from app.services.normalization.normalization_service import run_normalization

# ✅ Cache Layer
from app.services.cache.cache_service import CacheService

router = APIRouter()
cache_service = CacheService()


@router.post("/input")
async def handle_input(
    text: Optional[str] = Form(None),
    user_id: str = Form(...),
    audio: Optional[UploadFile] = File(None),
    file: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None)
):
    """
    PIPELINE:
    Input → Preprocessing → Normalization → Cache → Response
    """

    # Step 1: Input Handling
    input_result = process_input(text, audio, file, image, user_id)

    if not input_result.get("valid"):
        return input_result

    # Step 2: Preprocessing
    preprocessed_data = run_preprocessing(input_result)

    # Step 3: Normalization
    normalized_data = run_normalization(preprocessed_data)

    # ❌ Do not cache failed responses
    if normalized_data.get("status") == "failed":
        return normalized_data

    # Step 4: Cache Check
    cache_result = cache_service.check_cache(
        normalized_data,
        user_id=normalized_data.get("user_id")
    )

    # ✅ CACHE HIT (FIXED RESPONSE STRUCTURE)
    if cache_result["cache_hit"]:
        cached_response = cache_result["data"]

        # 🔥 Update request_id for current request
        cached_response["request_id"] = normalized_data["request_id"]

        # 🔥 Add cache source flag
        cached_response["source"] = "cache"

        return cached_response

    # CACHE MISS (temporary: return normalized data)
    final_response = normalized_data

    # Step 5: Store Cache
    cache_service.store_cache(
        cache_result["key"],
        final_response
    )

    return final_response