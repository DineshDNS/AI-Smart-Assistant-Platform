
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
                self.keyword_to_action[kw] = action
                self.all_keywords.append(kw)

    # =========================
    # 🔥 FUZZY MATCH
    # =========================
    def fuzzy_match(self, word: str, threshold: float = 0.75):
        matches = difflib.get_close_matches(
            word, self.all_keywords, n=1, cutoff=threshold
        )
        return matches[0] if matches else None

    # =========================
    # 🔥 MAIN EXTRACTION (ORDER SAFE)
    # =========================
    def extract_actions(self, text: str) -> list:
        text = normalize_text(text or "")

        actions = []
        seen = set()

        # =========================
        # 1. PHRASE MATCH (ORDER BASED)
        # =========================
        for phrase, action in PHRASE_MAP.items():
            if phrase in text and action not in seen:
                actions.append(action)
                seen.add(action)

        # =========================
        # 2. WORD-LEVEL MATCH (ORDER PRESERVED)
        # =========================
        words = text.split()

        for word in words:

            # 🔹 Exact match
            if word in self.keyword_to_action:
                action = self.keyword_to_action[word]

                if action not in seen:
                    actions.append(action)
                    seen.add(action)
                continue

            # 🔹 Fuzzy match (typo handling)
            matched = self.fuzzy_match(word)

            if matched:
                action = self.keyword_to_action.get(matched)

                if action and action not in seen:
                    actions.append(action)
                    seen.add(action)

        return actions

