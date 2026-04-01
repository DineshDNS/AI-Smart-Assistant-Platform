
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
        memory = intent_output.get("memory", {})  # 🔥 PASS MEMORY

        tasks = self.mapper.map_tasks(actions, data, instruction, memory)

        tasks, execution_type = self.resolver.resolve(tasks)

        plan = self.executor.build(tasks, execution_type)

        return plan

