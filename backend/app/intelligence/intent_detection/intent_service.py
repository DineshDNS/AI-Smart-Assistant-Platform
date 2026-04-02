from app.intelligence.intent_detection.action_extractor import ActionExtractor


class IntentService:

    def __init__(self):
        self.extractor = ActionExtractor()

    def normalize_text(self, text: str) -> str:
        return (text or "").lower().strip()

    # =========================
    # 🔥 GREETING DETECTION
    # =========================
    def is_greeting(self, text: str) -> bool:
        greetings = ["hi", "hello", "hey", "how are you", "what's up"]
        return any(g in text for g in greetings)

    # =========================
    # 🔥 MAIN INTENT
    # =========================
    def detect_intent(self, payload: dict):

        instruction = payload.get("instruction", {})
        instruction_text = instruction.get("raw", "")

        data = payload.get("data", [])

        instruction_text = self.normalize_text(instruction_text)

        # =========================
        # 🔥 IMAGE ONLY → DESCRIBE
        # =========================
        has_image = any(
            d.get("metadata", {}).get("source") == "image"
            for d in data
        )

        if not instruction_text and has_image:
            actions = ["describe"]

        # =========================
        # 🔥 GREETING
        # =========================
        elif self.is_greeting(instruction_text):
            actions = ["conversation"]

        # =========================
        # 🔥 QUESTION
        # =========================
        elif instruction_text.startswith(("what", "why", "how")):
            actions = ["explain"]

        # =========================
        # 🔥 ACTION EXTRACTION
        # =========================
        else:
            actions = self.extractor.extract_actions(instruction_text)

            # 🔥 FIX: fallback → conversation (NOT explain)
            if not actions:
                actions = ["conversation"]

        # =========================
        # FINAL OUTPUT
        # =========================
        return {
            **payload,
            "intent": {
                "type": "conversation" if actions[0] == "conversation" else "task",
                "complexity": "single",
                "confidence": 0.95,
                "source": "rule"
            },
            "actions": [{"name": actions[0]}],
            "instruction": {
                "text": [actions[0]],
                "raw": instruction_text,
                "source": instruction.get("source")
            }
        }