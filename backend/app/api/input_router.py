from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional

from app.services.input_handler_service import process_input
from app.services.preprocessing.preprocessing_service import run_preprocessing
from app.services.normalization.normalization_service import run_normalization
from app.services.cache.cache_service import CacheService

# 🔥 MEMORY
from app.memory.memory_manager import MemoryManager

# 🔥 INTELLIGENCE LAYERS
from app.intelligence.intent_detection.intent_service import IntentService
from app.intelligence.task_planner.planner_service import PlannerService

# 🔥 NEW: AGENT CONTROLLER
from app.agents.agent_controller import AgentController


router = APIRouter()

cache_service = CacheService()

# 🔥 Initialize once (performance optimized)
memory_manager = MemoryManager()
intent_service = IntentService()
planner_service = PlannerService()
agent_controller = AgentController()   # ✅ NEW


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
    Input → Preprocessing → Normalization → Cache → Memory → Intent → Task Planner → Agent Controller → Response
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

        cached_response["request_id"] = normalized_data["request_id"]
        cached_response["source"] = "cache"
        cached_response["cache"] = {
            "hit": True,
            "key": cache_result["key"]
        }

        return cached_response

    # =========================
    # STEP 5: MEMORY LAYER
    # =========================
    enriched_data = memory_manager.process(normalized_data)

    # =========================
    # STEP 6: INTENT DETECTION
    # =========================
    intent_output = intent_service.detect_intent(enriched_data)

    # =========================
    # STEP 7: TASK PLANNING
    # =========================
    task_plan = planner_service.plan(intent_output)

    # =========================
    # STEP 8: AGENT CONTROLLER 🔥 NEW
    # =========================
    agent_input = {
        **intent_output,
        "task_plan": task_plan,
        "memory": enriched_data.get("memory", {}),
        "data": intent_output.get("data", []),
    }

    agent_output = agent_controller.run(agent_input)

    # =========================
    # FINAL RESPONSE BUILD
    # =========================
    final_response = {
        **agent_output,
        "source": "system",
        "cache": {
            "hit": False,
            "key": cache_result["key"]
        }
    }

    # =========================
    # STEP 9: CACHE STORE
    # =========================
    cache_service.store_cache(
        cache_result["key"],
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