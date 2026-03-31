
from app.intelligence.task_planner.constants import ACTION_TARGET_MAP, TRANSFORMATION_KEYWORDS


class TaskMapper:

    def detect_output_type(self, instruction: str):
        instruction = instruction.lower()

        for output, phrases in TRANSFORMATION_KEYWORDS.items():
            for phrase in phrases:
                if phrase in instruction:
                    return output

        return None

    def map_tasks(self, actions, data, instruction):

        tasks = []
        task_id = 1

        output_type = self.detect_output_type(instruction)

        for action_obj in actions:
            action = action_obj["name"]

            possible_targets = ACTION_TARGET_MAP.get(action, [])

            matched = False

            for idx, item in enumerate(data):
                data_type = item.get("type")

                if data_type in possible_targets:
                    matched = True

                    task = {
                        "task_id": f"task_{task_id}",
                        "action": action,
                        "target": data_type,
                        "data_ref": idx,
                        "status": "pending"
                    }

                    # 🔥 transformation support
                    if action == "convert":
                        task["input_type"] = data_type
                        task["output_type"] = output_type or "unknown"

                    tasks.append(task)
                    task_id += 1

            # 🔴 fallback if no data matched
            if not matched:
                task = {
                    "task_id": f"task_{task_id}",
                    "action": action,
                    "target": "text",
                    "data_ref": None,
                    "status": "pending"
                }

                if action == "convert":
                    task["input_type"] = "text"
                    task["output_type"] = output_type or "unknown"

                tasks.append(task)
                task_id += 1

        return tasks

