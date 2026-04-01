from app.agents.tool_selector import select_tool
from app.agents.prompt_builder import build_prompt
from app.agents.execution_orchestrator import build_execution_steps
from app.agents.reasoning_engine import process_tasks
from app.agents.constants import LLM_CONFIG, DEFAULT_STRATEGY


class AgentController:

    def run(self, payload: dict) -> dict:

        task_plan = payload.get("task_plan", {})
        tasks = task_plan.get("tasks", [])
        execution_strategy = task_plan.get("execution", DEFAULT_STRATEGY)

        # =========================
        # EDGE CASE: NO TASKS
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
        # STEP 1: REASONING
        # =========================
        tasks = process_tasks(tasks)

        # =========================
        # 🔥 SAFE MEMORY CONTEXT
        # =========================
        memory = payload.get("memory", {})
        if not memory.get("context"):
            memory["context"] = payload.get("instruction", {}).get("raw", "")

        # =========================
        # STEP 2: EXECUTION STEPS
        # =========================
        steps = build_execution_steps(
            tasks=tasks,
            select_tool=select_tool,
            build_prompt=build_prompt,
            data=payload.get("data", []),
            memory=memory
        )

        # =========================
        # STEP 3: FINAL PLAN
        # =========================
        payload["agent_plan"] = {
            "execution_steps": steps,
            "execution_strategy": execution_strategy,
            "llm_config": LLM_CONFIG
        }

        payload["status"] = "agent_planned"

        return payload