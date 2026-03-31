from transformers import pipeline

class ModelEngine:

    def __init__(self):
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )

        self.labels = [
            "summarize text",
            "analyze data",
            "translate language",
            "generate content",
            "explain concept",
            "describe image",
            "extract information",
            "predict outcome",
            "compare items"
        ]

    def predict_action(self, text: str):
        result = self.classifier(text, self.labels)

        label = result["labels"][0]
        score = result["scores"][0]

        action = label.split()[0]  # normalize label → action

        return action, score