from app.services.normalization.instruction_extractor import extract_instruction
from app.services.normalization.data_builder import build_data
from app.services.normalization.summary_builder import build_summary
from app.services.normalization.validators import validate_preprocessing_output


def run_normalization(preprocessed_data: dict) -> dict:
    try:
        validate_preprocessing_output(preprocessed_data)

        instruction_raw = extract_instruction(preprocessed_data)

        instruction = {
            "text": instruction_raw.get("text", ""),
            "raw": instruction_raw.get("raw_text") or instruction_raw.get("text", ""),  # 🔥 FIX
            "source": instruction_raw.get("source", "default"),
            "type": instruction_raw.get("type", "default")
        }

        data = build_data(preprocessed_data, instruction_raw)
        summary = build_summary(data)

        return {
            "request_id": preprocessed_data.get("request_id"),
            "user_id": preprocessed_data.get("user_id"),
            "session_id": preprocessed_data.get("session_id"),
            "status": "normalized",
            "instruction": instruction,
            "data": data,
            "context": [],
            "summary": summary,
            "errors": preprocessed_data.get("errors", [])
        }

    except Exception as e:
        return {
            "request_id": preprocessed_data.get("request_id"),
            "user_id": preprocessed_data.get("user_id"),
            "session_id": preprocessed_data.get("session_id"),
            "status": "failed",
            "error": str(e)
        }