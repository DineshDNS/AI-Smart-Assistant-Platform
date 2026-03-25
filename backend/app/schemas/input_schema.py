from pydantic import BaseModel
from typing import Optional

class InputRequest(BaseModel):
    text: Optional[str] = None
    user_id: str

class InputResponse(BaseModel):
    request_id: str
    timestamp: str
    user_id: str
    status: str
    valid: bool
    input_types: list
    data: dict
    metadata: dict
    processing_flags: dict
    errors: list