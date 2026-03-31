
class DependencyResolver:

    def resolve(self, tasks):

        # 🔥 simple rule: transcribe → summarize
        actions = [t["action"] for t in tasks]

        if "transcribe" in actions and "summarize" in actions:

            transcribe_task = next(t for t in tasks if t["action"] == "transcribe")

            for task in tasks:
                if task["action"] == "summarize":
                    task["depends_on"] = transcribe_task["task_id"]

            return tasks, "sequential"

        return tasks, "parallel"

