from app.intelligence.task_planner.constants import TRANSFORMATION_KEYWORDS


class TaskMapper:

    def detect_output_type(self, instruction: str):
        instruction = (instruction or "").lower()

        for output, phrases in TRANSFORMATION_KEYWORDS.items():
            for phrase in phrases:
                if phrase in instruction:
                    return output

        return None

    def detect_conversion_direction(self, instruction: str):
        instruction = (instruction or "").lower()

        if "audio to text" in instruction or "speech to text" in instruction:
            return "audio", "text"

        if "text to audio" in instruction or "text to speech" in instruction:
            return "text", "audio"

        if "to audio" in instruction:
            return "text", "audio"

        if "to text" in instruction:
            return "audio", "text"

        return None, None

    def is_contextual_request(self, instruction: str):
        instruction = (instruction or "").lower()

        pronouns = ["it", "this", "that", "these", "those"]
        time_refs = ["previous", "last", "latest", "earlier", "recent", "before", "past"]
        positional_refs = ["above", "below", "before this", "after that"]

        contextual_phrases = [
            "the result", "that result", "this result",
            "previous result", "last result",
            "the output", "that output", "this output",
            "previous output", "generated output",
            "what you generated", "what you created",
            "earlier output", "recent output"
        ]

        if any(p in instruction for p in contextual_phrases):
            return True

        words = instruction.split()
        return any(w in (pronouns + time_refs + positional_refs) for w in words)

    def is_derived_context(self, instruction: str):
        instruction = (instruction or "").lower()

        derived_keywords = [
            "summary", "result", "output", "report",
            "analysis", "data", "response"
        ]

        return any(k in instruction for k in derived_keywords)

    def get_memory_output_type(self, memory: dict):
        short_term = memory.get("short_term", [])

        if not short_term:
            return None

        last = short_term[-1]
        summary = last.get("response", {}).get("summary", {})
        modalities = summary.get("modalities", [])

        if "document" in modalities:
            return "document"
        if "image" in modalities:
            return "image"
        if "text" in modalities:
            return "text"

        return "text"

    # =========================
    # 🔥 MAIN MAPPER (FINAL)
    # =========================
    def map_tasks(self, actions, data, instruction, memory=None, completed_steps=None):

        tasks = []
        task_id = 1

        instruction = instruction or ""
        output_type = self.detect_output_type(instruction)

        action_to_task = {}
        input_type = data[0]["type"] if data else "text"

        is_context = self.is_contextual_request(instruction)
        is_derived = self.is_derived_context(instruction)

        memory_input_type = self.get_memory_output_type(memory or {})

        completed_steps = completed_steps or set()

        for action_obj in actions:
            action = action_obj.get("name")

            # =========================
            # 🔥 SKIP DUPLICATES
            # =========================
            if action == "transcribe" and "transcribe" in completed_steps:
                continue

            if action in ["clean", "normalize"] and "clean" in completed_steps:
                continue

            # =========================
            # 🟢 CONVERSATION
            # =========================
            if action == "conversation":
                tasks.append({
                    "task_id": f"task_{task_id}",
                    "action": "conversation",
                    "input": {"type": "text", "source": "input"},
                    "output": {"type": "text"},
                    "status": "pending"
                })
                task_id += 1
                continue

            # =========================
            # 🔴 CONVERT (FINAL FIX)
            # =========================
            if action == "convert":

                input_detected, output_detected = self.detect_conversion_direction(instruction)

                # 🔥 SKIP AUDIO → TEXT (already transcribed)
                if (
                    input_detected == "audio"
                    and output_detected == "text"
                    and "transcribe" in completed_steps
                ):
                    continue

                if (is_context or is_derived) and memory_input_type:
                    source = "memory"
                    input_type_final = memory_input_type
                else:
                    source = (
                        action_to_task.get("generate")
                        or action_to_task.get("translate")
                        or action_to_task.get("summarize")
                    )
                    input_type_final = input_detected or input_type

                output_type_final = output_detected or output_type or "audio"

                tasks.append({
                    "task_id": f"task_{task_id}",
                    "action": "convert",
                    "input": {
                        "type": input_type_final,
                        "source": source or "input"
                    },
                    "output": {
                        "type": output_type_final
                    },
                    "status": "pending",
                    "depends_on": source if source not in ["memory", None] else None
                })

                task_id += 1
                continue

            # =========================
            # 🟡 DEFAULT
            # =========================
            tasks.append({
                "task_id": f"task_{task_id}",
                "action": action,
                "input": {
                    "type": input_type,
                    "source": "input"
                },
                "output": {"type": "text"},
                "status": "pending"
            })

            task_id += 1

        return tasks