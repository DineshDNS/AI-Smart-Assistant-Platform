from app.memory.config import MIN_INSTRUCTION_LENGTH


class MemoryFilter:

    def filter(self, items):
        seen = set()
        result = []

        for item in items:
            text = item.get("text", "").strip()

            # ❌ Skip empty
            if not text:
                continue

            # ❌ Skip short
            if len(text.split()) <= MIN_INSTRUCTION_LENGTH:
                continue

            # ❌ Skip duplicates
            if text in seen:
                continue

            seen.add(text)
            result.append(item)

        return result