from pydantic import BaseModel
from typing import Any, Dict, List


class PreprocessingResponse(BaseModel):
    request_id: str
    user_id: str
    status: str
    processed_data: Dict[str, Any]
    processing_summary: Dict[str, bool]
    errors: List[Dict[str, str]]