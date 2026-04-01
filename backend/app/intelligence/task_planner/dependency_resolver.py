
class DependencyResolver:

    def resolve(self, tasks):

        has_dependencies = any(task.get("depends_on") for task in tasks)

        if has_dependencies:
            return tasks, "graph"

        return tasks, "parallel"

