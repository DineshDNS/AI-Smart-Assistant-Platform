from sentence_transformers import SentenceTransformer
from app.memory.config import EMBEDDING_MODEL

class EmbeddingModel:

    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def encode(self, text):
        return self.model.encode(text).tolist()