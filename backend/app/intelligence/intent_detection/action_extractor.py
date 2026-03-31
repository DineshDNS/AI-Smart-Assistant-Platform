
from app.intelligence.intent_detection.constants import ACTION_GROUPS, PHRASE_MAP
from app.intelligence.intent_detection.utils import normalize_text
import difflib


class ActionExtractor:

    def __init__(self):
        # Flatten all keywords
        self.keyword_to_action = {}
        self.all_keywords = []

        for action, keywords in ACTION_GROUPS.items():
            for kw in keywords:
                self.keyword_to_action[kw] = action
                self.all_keywords.append(kw)

    def fuzzy_match(self, word: str, threshold: float = 0.75):
        matches = difflib.get_close_matches(word, self.all_keywords, n=1, cutoff=threshold)
        return matches[0] if matches else None

    def extract_actions(self, text: str) -> list:
        text = normalize_text(text)
        actions = set()

        words = text.split()

        # =========================
        # 1. PHRASE MATCH (HIGH PRIORITY)
        # =========================
        for phrase, action in PHRASE_MAP.items():
            if phrase in text:
                actions.add(action)

        # =========================
        # 2. EXACT KEYWORD MATCH
        # =========================
        for kw, action in self.keyword_to_action.items():
            if kw in text:
                actions.add(action)

        # =========================
        # 3. FUZZY WORD MATCH (TYPO FIX)
        # =========================
        for word in words:
            matched = self.fuzzy_match(word)

            if matched:
                action = self.keyword_to_action.get(matched)
                if action:
                    actions.add(action)

        return list(actions)

