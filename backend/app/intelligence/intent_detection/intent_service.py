
from app.intelligence.intent_detection.action_extractor import ActionExtractor
from app.intelligence.intent_detection.model_engine import ModelEngine
from app.intelligence.intent_detection.intent_classifier import IntentClassifier


class IntentService:

    def __init__(self):
        self.extractor = ActionExtractor()
        self.model_engine = ModelEngine()
        self.classifier = IntentClassifier()

    # =========================
    # 🔥 WEAK INPUT DETECTION
    # =========================
    def is_meaningless_input(self, text: str):
        if not text:
            return True

        text = text.strip().lower()

        weak_words = {
            "ok", "okay", "yes", "yeah", "yep",
            "sure", "hmm", "hmmm", "huh",
            "continue", "go ahead", "proceed",
            "fine", "alright", "done"
        }

        if text in weak_words:
            return True

        # very short meaningless
        if len(text.split()) <= 1:
            return True

        return False

    # =========================
    # 🔹 DATA FALLBACK
    # =========================
    def infer_from_data(self, actions, data):
        if actions:
            return actions

        data_types = [d.get("type") for d in data]
        inferred = []

        if "document" in data_types:
            inferred.append("summarize")

        if "image" in data_types:
            inferred.append("describe")

        if "audio" in data_types:
            inferred.append("transcribe")

        return inferred

    # =========================
    # 🔥 MAIN FUNCTION
    # =========================
    def detect_intent(self, payload: dict):

        instruction = payload.get("instruction", {})
        instruction_text = instruction.get("text", "")

        request_id = payload.get("request_id")
        user_id = payload.get("user_id")
        session_id = payload.get("session_id")

        # =========================
        # 🔥 HANDLE MEANINGLESS INPUT
        # =========================
        if self.is_meaningless_input(instruction_text):

            return {
                "status": "intent_detected",

                "request_id": request_id,
                "user_id": user_id,
                "session_id": session_id,

                "intent": {
                    "type": "conversation",
                    "complexity": "single",
                    "confidence": 1.0,
                    "source": "rule"
                },

                "actions": [],

                "instruction": {
                    "text": [],
                    "raw": instruction_text,
                    "source": "conversation"
                },

                "data": payload.get("data"),
                "summary": payload.get("summary"),
                "memory": payload.get("memory"),

                # 🔥 DEFAULT RESPONSE
                "response_hint": "Please provide a clear instruction so I can help you."
            }

        # =========================
        # STEP 1: ACTION EXTRACTION
        # =========================
        actions = self.extractor.extract_actions(instruction_text)

        source = "rule"
        confidence = 0.95

        # =========================
        # STEP 2: DATA FALLBACK
        # =========================
        if not actions:
            actions = self.infer_from_data(actions, payload.get("data", []))

        # =========================
        # STEP 3: ML FALLBACK (SAFE)
        # =========================
        if not actions and instruction_text.strip():
            action, score = self.model_engine.predict_action(instruction_text)

            if score >= 0.6:
                actions = [action]
                confidence = float(score)
                source = "model"

        # =========================
        # STEP 4: INTENT TYPE
        # =========================
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
                "confidence": confidence,
                "source": source
            },

            "actions": [{"name": a} for a in actions],

            "instruction": {
                "text": actions if actions else [],
                "raw": instruction_text,
                "source": instruction.get("source")
            },

            "data": payload.get("data"),
            "summary": payload.get("summary"),
            "memory": payload.get("memory")
        }

