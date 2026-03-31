class IntentClassifier:

    def classify(self, actions: list, is_conversation: bool):

        if is_conversation:
            return "conversation"

        if not actions:
            return "unknown"

        if len(actions) == 1:
            return "task"

        return "multi_task"