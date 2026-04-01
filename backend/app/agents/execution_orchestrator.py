def build_execution_steps(tasks, select_tool, build_prompt, data, memory):

    steps = []
    task_to_step = {}

    memory_context = memory.get("context", "") if memory else ""

    for index, task in enumerate(tasks):

        step_id = f"step_{index+1}"
        task_id = task.get("task_id")

        action = task.get("action")
        input_info = task.get("input", {})

        input_type = input_info.get("type", "text")

        if input_type == "summary" and not data:
            input_type = "text"

        tool = select_tool(action, input_type)

        effective_data = data.copy()

        if not effective_data:
            effective_data = [{
                "type": "text",
                "content": memory_context or ""
            }]

        prompt = build_prompt(
            action,
            tool,
            effective_data,
            memory_context
        )

        depends_on_task = task.get("depends_on")
        depends_on_step = task_to_step.get(depends_on_task)

        step = {
            "step_id": step_id,
            "task_id": task_id,
            "tool": tool,
            "input": {
                "type": input_type,
                "source": "input"
            },
            "prompt": prompt,
            "depends_on": depends_on_step
        }

        steps.append(step)
        task_to_step[task_id] = step_id

    return steps