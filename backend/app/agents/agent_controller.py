from app.agents.tool_selector import select_tool
from app.agents.prompt_builder import build_prompt
from app.agents.execution_orchestrator import build_execution_steps
from app.agents.reasoning_engine import process_tasks
from app.agents.constants import LLM_CONFIG, DEFAULT_STRATEGY


class AgentController:

    def is_relevant_memory(self, context: str, instruction: str) -> bool:
        if not context or not instruction:
            return False
        return any(word in context.lower() for word in instruction.lower().split())

    def has_audio_input(self, data: list) -> bool:
        return any(item.get("metadata", {}).get("source") == "audio" for item in data)

    def run(self, payload: dict) -> dict:

        task_plan = payload.get("task_plan", {})
        tasks = task_plan.get("tasks", [])
        execution_strategy = task_plan.get("execution", DEFAULT_STRATEGY)

        data = payload.get("data", [])
        instruction_text = payload.get("instruction", {}).get("raw", "")

        # =========================
        # 🔥 DIRECT OUTPUT (AUDIO → TEXT)
        # =========================
        if self.has_audio_input(data) and ("to text" in instruction_text.lower() or "convert" in instruction_text.lower()):
            for item in data:
                if item.get("metadata", {}).get("source") == "audio":
                    return {
                        **payload,
                        "status": "completed",
                        "final_output": item.get("content"),
                        "agent_plan": {
                            "execution_steps": [],
                            "execution_strategy": "none",
                            "llm_config": LLM_CONFIG
                        }
                    }

        # =========================
        # NO TASKS
        # =========================
        if not tasks:
            payload["agent_plan"] = {
                "execution_steps": [],
                "execution_strategy": "none",
                "llm_config": LLM_CONFIG
            }
            payload["status"] = "agent_planned"
            return payload

        # =========================
        # 🔥 MEMORY CONTROL
        # =========================
        memory = payload.get("memory", {})
        context = memory.get("context", "")

        if self.has_audio_input(data):
            memory["context"] = instruction_text
        elif not self.is_relevant_memory(context, instruction_text):
            memory["context"] = instruction_text
        elif not context:
            memory["context"] = instruction_text

        # =========================
        # BUILD EXECUTION
        # =========================
        tasks = process_tasks(tasks)

        steps = build_execution_steps(
            tasks=tasks,
            select_tool=select_tool,
            build_prompt=build_prompt,
            data=data,
            memory=memory
        )

        payload["agent_plan"] = {
            "execution_steps": steps,
            "execution_strategy": execution_strategy,
            "llm_config": LLM_CONFIG
        }

        payload["status"] = "agent_planned"

        return payload