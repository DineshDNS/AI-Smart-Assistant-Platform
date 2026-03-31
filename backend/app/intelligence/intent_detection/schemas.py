from pydantic import BaseModel
from typing import List, Dict, Any

class IntentOutput(BaseModel):
    intent: Dict[str, Any]
    actions: List[str]
    instruction: Dict[str, Any]
    data: List[Any]
    summary: Dict[str, Any]
    memory: Dict[str, Any]