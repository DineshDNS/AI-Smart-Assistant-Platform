from pydantic import BaseModel
from typing import List, Dict, Any


class Instruction(BaseModel):
    text: str
    tokens: List[str]


class DataItem(BaseModel):
    type: str
    content: Any
    metadata: Dict


class NormalizedOutput(BaseModel):
    request_id: str
    user_id: str
    status: str
    instruction: Instruction
    data: List[DataItem]
    context: List
    summary: Dict
    errors: List