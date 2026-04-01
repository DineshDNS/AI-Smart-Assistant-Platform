from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class ExecutionStep(BaseModel):
    step_id: str
    task_id: str
    tool: str
    input: Dict[str, Any]
    prompt: str
    depends_on: Optional[str] = None


class AgentPlan(BaseModel):
    execution_steps: List[ExecutionStep]
    execution_strategy: str
    llm_config: Dict[str, Any]


class AgentResponse(BaseModel):
    status: str
    request_id: str
    user_id: str
    session_id: str

    intent: Dict[str, Any]
    actions: List[Dict[str, Any]]
    instruction: Dict[str, Any]
    data: List[Dict[str, Any]]
    summary: Dict[str, Any]
    memory: Dict[str, Any]
    task_plan: Dict[str, Any]

    agent_plan: AgentPlan

    response_hint: Optional[str] = None
    source: str
    cache: Dict[str, Any]