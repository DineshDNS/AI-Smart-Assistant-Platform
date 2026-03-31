
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

        # STEP 1: map tasks
        tasks = self.mapper.map_tasks(actions, data, instruction)

        # STEP 2: resolve dependencies
        tasks, execution_type = self.resolver.resolve(tasks)

        # STEP 3: build execution plan
        plan = self.executor.build(tasks, execution_type)

        return plan

