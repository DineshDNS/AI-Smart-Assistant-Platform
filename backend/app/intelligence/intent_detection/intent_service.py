from app.intelligence.intent_detection.action_extractor import ActionExtractor


class IntentService:

    def __init__(self):
        self.extractor = ActionExtractor()

    def normalize_text(self, text: str) -> str:
        return (text or "").lower().strip()

    # =========================
    # GREETING
    # =========================
    def is_greeting(self, text: str) -> bool:
        greetings = ["hi", "hello", "hey", "how are you", "what's up"]
        return any(g in text for g in greetings)

    # =========================
    # FILE DETECTION
    # =========================
    def has_file(self, data: list) -> bool:
        return any(
            d.get("metadata", {}).get("source") == "file"
            for d in data
        )

    # =========================
    # MAIN INTENT
    # =========================
    def detect_intent(self, payload: dict):

        instruction = payload.get("instruction", {})
        instruction_text = instruction.get("raw", "")
        data = payload.get("data", [])

        instruction_text = self.normalize_text(instruction_text)

        has_file = self.has_file(data)

        # =========================
        # 🔥 GREETING
        # =========================
        if self.is_greeting(instruction_text):
            action = "conversation"

        # =========================
        # 🔥 FILE + SUMMARIZE (CRITICAL FIX)
        # =========================
        elif has_file and "summarize" in instruction_text:
            action = "summarize"

        # =========================
        # 🔥 QUESTION
        # =========================
        elif instruction_text.startswith(("what", "why", "how")):
            action = "explain"

        # =========================
        # 🔥 EXTRACT ACTION
        # =========================
        else:
            actions = self.extractor.extract_actions(instruction_text)

            # 🔥 FIXED FALLBACK
            if not actions:
                action = "explain"   # ✅ NOT conversation
            else:
                action = actions[0]


        # =========================
        # FINAL OUTPUT
        # =========================
        return {
            **payload,
            "intent": {
                "type": "conversation" if action == "conversation" else "task",
                "complexity": "single",
                "confidence": 0.95,
                "source": "rule"
            },
            "actions": [{"name": action}],
            "instruction": {
                "text": [action],
                "raw": instruction_text,
                "source": instruction.get("source")
            }
        }