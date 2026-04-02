from app.intelligence.task_planner.task_mapper import TaskMapper
from app.intelligence.task_planner.dependency_resolver import DependencyResolver
from app.intelligence.task_planner.execution_planner import ExecutionPlanner


class PlannerService:

    def __init__(self):
        self.mapper = TaskMapper()
        self.resolver = DependencyResolver()
        self.executor = ExecutionPlanner()

    def plan(self, intent_output: dict):

        actions = intent_output.get("actions", [])
        data = intent_output.get("data", [])
        instruction = intent_output.get("instruction", {}).get("raw", "")
        memory = intent_output.get("memory", {})

        # =========================
        # 🔥 DETECT COMPLETED STEPS
        # =========================
        completed_steps = set()

        for item in data:
            source = item.get("metadata", {}).get("source")

            if source == "audio":
                completed_steps.add("transcribe")

            if source == "text":
                completed_steps.add("clean")

        # =========================
        # TASK MAPPING
        # =========================
        tasks = self.mapper.map_tasks(
            actions,
            data,
            instruction,
            memory,
            completed_steps
        )

        # =========================
        # 🔥 DIRECT OUTPUT SUPPORT
        # =========================
        if not tasks:
            return {
                "status": "task_planned",
                "tasks": [],
                "execution": "none",
                "meta": {
                    "total_tasks": 0,
                    "completed_steps": list(completed_steps),
                    "direct_output": True
                }
            }

        tasks, execution_type = self.resolver.resolve(tasks)

        plan = self.executor.build(tasks, execution_type)

        plan["meta"]["completed_steps"] = list(completed_steps)

        return plan