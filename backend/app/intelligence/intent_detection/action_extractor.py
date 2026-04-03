from app.intelligence.intent_detection.constants import ACTION_GROUPS, PHRASE_MAP
from app.intelligence.intent_detection.utils import normalize_text
import difflib


class ActionExtractor:

    def __init__(self):
        # 🔥 Flatten keywords
        self.keyword_to_action = {}
        self.all_keywords = []

        for action, keywords in ACTION_GROUPS.items():
            for kw in keywords:
                kw = kw.lower()
                self.keyword_to_action[kw] = action
                self.all_keywords.append(kw)

        # 🔥 HIGH PRIORITY DIRECT WORDS (CRITICAL FIX)
        self.priority_map = {
            "summarize": "summarize",
            "summary": "summarize",
            "explain": "explain",
            "analysis": "analyze",
            "analyze": "analyze",
            "describe": "describe",
            "detect": "detect",
            "convert": "convert",
            "translate": "translate",
        }

    # =========================
    # 🔥 FUZZY MATCH
    # =========================
    def fuzzy_match(self, word: str, threshold: float = 0.75):
        matches = difflib.get_close_matches(
            word, self.all_keywords, n=1, cutoff=threshold
        )
        return matches[0] if matches else None

    # =========================
    # 🔥 DIRECT PRIORITY MATCH (NEW)
    # =========================
    def priority_match(self, text: str):
        for key, action in self.priority_map.items():
            if key in text:
                return [action]
        return []

    # =========================
    # 🔥 FILE-AWARE BOOST (NEW)
    # =========================
    def file_context_boost(self, text: str):
        """
        Detect implicit file-based actions
        """
        if "file" in text or "document" in text or "pdf" in text:

            if "summarize" in text or "summary" in text:
                return ["summarize"]

            if "explain" in text or text.startswith(("what", "why", "how")):
                return ["explain"]

            if "analyze" in text:
                return ["analyze"]

        return []

    # =========================
    # 🔥 MAIN EXTRACTION (FINAL)
    # =========================
    def extract_actions(self, text: str) -> list:

        text = normalize_text(text or "")
        actions = []
        seen = set()

        # =========================
        # 0. 🔥 FILE CONTEXT BOOST (FIRST PRIORITY)
        # =========================
        boosted = self.file_context_boost(text)
        if boosted:
            return boosted

        # =========================
        # 1. 🔥 PRIORITY DIRECT MATCH
        # =========================
        priority = self.priority_match(text)
        if priority:
            return priority

        # =========================
        # 2. PHRASE MATCH
        # =========================
        for phrase, action in PHRASE_MAP.items():
            if phrase in text and action not in seen:
                actions.append(action)
                seen.add(action)

        # =========================
        # 3. WORD-LEVEL MATCH
        # =========================
        words = text.split()

        for word in words:

            # Exact match
            if word in self.keyword_to_action:
                action = self.keyword_to_action[word]

                if action not in seen:
                    actions.append(action)
                    seen.add(action)
                continue

            # Fuzzy match
            matched = self.fuzzy_match(word)

            if matched:
                action = self.keyword_to_action.get(matched)

                if action and action not in seen:
                    actions.append(action)
                    seen.add(action)

        return actions