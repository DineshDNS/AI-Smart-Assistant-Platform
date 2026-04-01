from app.intelligence.intent_detection.action_extractor import ActionExtractor
from app.intelligence.intent_detection.model_engine import ModelEngine
from app.intelligence.intent_detection.intent_classifier import IntentClassifier


class IntentService:

    def __init__(self):
        self.extractor = ActionExtractor()
        self.model_engine = ModelEngine()
        self.classifier = IntentClassifier()

    # =========================
    # 🔥 GREETING DETECTION (ROBUST)
    # =========================
    def is_greeting(self, text: str) -> bool:
        text = (text or "").lower().strip()

        BASE_GREETINGS = [
            "hi", "hello", "hey", "yo", "sup",
            "good morning", "good afternoon", "good evening",
            "how are you", "how's it going", "whats up",
            "what's up", "bye", "goodbye", "see you", "talk to you later",
            "take care", "nice talking to you"
        ]

        # ✅ phrase match anywhere
        if any(greet in text for greet in BASE_GREETINGS):
            return True

        # ✅ short informal patterns
        if len(text.split()) <= 3:
            informal_patterns = ["hi", "hey", "hello"]
            if any(p in text for p in informal_patterns):
                return True

        return False

    # =========================
    # 🔥 QUESTION → EXPLAIN
    # =========================
    def detect_question_intent(self, text: str):
        text = (text or "").lower().strip()

        question_keywords = ["what", "why", "how", "when", "where", "who", "which"]

        explain_phrases = [
            "explain", "tell me", "describe",
            "help me understand", "i want to understand",
            "can you explain", "could you explain"
        ]

        for phrase in explain_phrases:
            if phrase in text:
                return "explain"

        for word in question_keywords:
            if word in text:
                return "explain"

        return None

    # =========================
    # 🔥 MAIN INTENT DETECTION
    # =========================
    def detect_intent(self, payload: dict):

        instruction = payload.get("instruction", {})
        instruction_text = instruction.get("text", "")

        if isinstance(instruction_text, list):
            instruction_text = " ".join(instruction_text)

        instruction_text = instruction_text or ""

        request_id = payload.get("request_id")
        user_id = payload.get("user_id")
        session_id = payload.get("session_id")
        memory = payload.get("memory", {})

        # =========================
        # 🟢 GREETING → CONVERSATION
        # =========================
        if self.is_greeting(instruction_text):
            return {
                "status": "intent_detected",
                "request_id": request_id,
                "user_id": user_id,
                "session_id": session_id,
                "intent": {
                    "type": "conversation",
                    "complexity": "single",
                    "confidence": 0.95,
                    "source": "rule"
                },
                "actions": [{"name": "conversation"}],
                "instruction": {
                    "text": ["conversation"],
                    "raw": instruction_text,
                    "source": "conversation"
                },
                "data": payload.get("data"),
                "summary": payload.get("summary"),
                "memory": memory
            }

        # =========================
        # 🔵 QUESTION → EXPLAIN
        # =========================
        question_action = self.detect_question_intent(instruction_text)

        if question_action:
            return {
                "status": "intent_detected",
                "request_id": request_id,
                "user_id": user_id,
                "session_id": session_id,
                "intent": {
                    "type": "task",
                    "complexity": "single",
                    "confidence": 0.95,
                    "source": "question_rule"
                },
                "actions": [{"name": question_action}],
                "instruction": {
                    "text": [question_action],
                    "raw": instruction_text,
                    "source": "question"
                },
                "data": payload.get("data"),
                "summary": payload.get("summary"),
                "memory": memory
            }

        # =========================
        # 🟡 ACTION EXTRACTION
        # =========================
        actions = self.extractor.extract_actions(instruction_text)

        intent_type = self.classifier.classify(actions, False)
        complexity = "single" if len(actions) <= 1 else "multi"

        return {
            "status": "intent_detected",
            "request_id": request_id,
            "user_id": user_id,
            "session_id": session_id,
            "intent": {
                "type": intent_type,
                "complexity": complexity,
                "confidence": 0.95,
                "source": "rule"
            },
            "actions": [{"name": a} for a in actions],
            "instruction": {
                "text": actions if actions else [],
                "raw": instruction_text,
                "source": instruction.get("source")
            },
            "data": payload.get("data"),
            "summary": payload.get("summary"),
            "memory": memory
        }