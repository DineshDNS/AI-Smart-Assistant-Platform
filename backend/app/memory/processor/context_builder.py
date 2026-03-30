class ContextBuilder:

    def _format_summary(self, summary: dict) -> str:
        """
        Convert summary dict → readable text
        """
        if not summary:
            return "No data available."

        total = summary.get("total_items", 0)
        modalities = summary.get("modalities", [])

        if total == 0:
            return "No relevant data found."

        return f"{total} items processed with types: {', '.join(modalities)}"

    def build(self, short_term, long_term):

        lines = []

        # 🔹 SHORT-TERM (conversation)
        for item in short_term:
            instruction = item.get("instruction", "")
            summary = item.get("response", {}).get("summary", {})

            formatted_summary = self._format_summary(summary)

            lines.append(f"User: {instruction}")
            lines.append(f"Assistant: {formatted_summary}")

        # 🔹 LONG-TERM (knowledge recall)
        for item in long_term:
            lines.append(f"Relevant: {item.get('text')}")

        return {
            "short_term": short_term,
            "long_term": long_term,
            "context": "\n".join(lines),
            "meta": {
                "short_count": len(short_term),
                "long_count": len(long_term)
            }
        }