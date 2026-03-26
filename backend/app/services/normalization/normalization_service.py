from app.services.normalization.instruction_extractor import extract_instruction
from app.services.normalization.data_builder import build_data
from app.services.normalization.summary_builder import build_summary
from app.services.normalization.validators import validate_preprocessing_output


def run_normalization(preprocessed_data: dict) -> dict:
    try:
        # ✅ Step 1: Validate input
        validate_preprocessing_output(preprocessed_data)

        # ✅ Step 2: Extract instruction (internal use)
        instruction_raw = extract_instruction(preprocessed_data)

        # ✅ Clean instruction for API response (remove internal fields)
        instruction = {
            "text": instruction_raw.get("text", ""),
            "tokens": instruction_raw.get("tokens", [])
        }

        # ✅ Step 3: Build data (uses internal extracted data)
        data = build_data(preprocessed_data, instruction_raw)

        # ✅ Step 4: Build summary
        summary = build_summary(data)

        # ✅ Final Output
        return {
            "request_id": preprocessed_data.get("request_id"),
            "user_id": preprocessed_data.get("user_id"),
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
            "status": "failed",
            "error": str(e)
        }