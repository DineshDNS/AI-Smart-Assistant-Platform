
from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional

from app.services.input_handler_service import process_input
from app.services.preprocessing.preprocessing_service import run_preprocessing
from app.services.normalization.normalization_service import run_normalization
from app.services.cache.cache_service import CacheService
from app.services.cache.cache_key_builder import build_cache_key

from app.memory.memory_manager import MemoryManager
from app.intelligence.intent_detection.intent_service import IntentService


router = APIRouter()

cache_service = CacheService()
memory_manager = MemoryManager()
intent_service = IntentService()


@router.post("/input")
async def handle_input(
    text: Optional[str] = Form(None),
    user_id: str = Form(...),
    session_id: str = Form(...),

    audio: Optional[List[UploadFile]] = File(None),
    file: Optional[List[UploadFile]] = File(None),
    image: Optional[List[UploadFile]] = File(None),
):

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
    # STEP 4: MEMORY
    # =========================
    enriched_data = memory_manager.process(normalized_data)

    # =========================
    # STEP 5: INTENT
    # =========================
    intent_output = intent_service.detect_intent(enriched_data)

    # =========================
    # STEP 6: CACHE KEY (SEMANTIC)
    # =========================
    cache_key = build_cache_key(
        normalized_data=normalized_data,
        intent_data=intent_output,
        user_id=normalized_data.get("user_id")
    )

    # =========================
    # STEP 7: CACHE CHECK
    # =========================
    cache_result = cache_service.check_cache_by_key(cache_key)

    # =========================
    # CACHE HIT
    # =========================
    if cache_result["cache_hit"]:
        cached = cache_result["data"]

        # Update metadata
        cached["request_id"] = normalized_data["request_id"]
        cached["user_id"] = normalized_data["user_id"]
        cached["session_id"] = normalized_data["session_id"]

        # 🔥 FIX: update RAW instruction
        cached["instruction"]["raw"] = normalized_data["instruction"]["text"]

        cached["source"] = "cache"
        cached["cache"] = {
            "hit": True,
            "key": cache_key
        }

        return cached

    # =========================
    # STEP 8: FINAL RESPONSE
    # =========================
    final_response = intent_output

    final_response["source"] = "system"
    final_response["cache"] = {
        "hit": False,
        "key": cache_key
    }

    # =========================
    # STEP 9: STORE CACHE
    # =========================
    cache_service.store_cache(
        cache_key,
        final_response
    )

    # =========================
    # STEP 10: MEMORY UPDATE
    # =========================
    memory_manager.update(
        normalized_data,
        final_response
    )

    return final_response

