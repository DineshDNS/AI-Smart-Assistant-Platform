
from app.memory.short_term.redis_memory import RedisMemory
from app.memory.long_term.embedding_model import EmbeddingModel
from app.memory.long_term.faiss_store import FaissStore
from app.memory.processor.memory_filter import MemoryFilter
from app.memory.processor.context_builder import ContextBuilder
from app.memory.retriever.semantic_search import SemanticSearch


class MemoryManager:

    def __init__(self):
        self.redis = RedisMemory()
        self.embedder = EmbeddingModel()
        self.faiss = FaissStore()
        self.filter = MemoryFilter()
        self.builder = ContextBuilder()
        self.search = SemanticSearch(self.faiss)

    # =========================
    # FETCH MEMORY
    # =========================
    def process(self, payload: dict):

        user_id = payload["user_id"]
        session_id = payload["session_id"]

        instruction = payload["instruction"].get("raw", "")

        # 🔥 SAFETY
        if isinstance(instruction, list):
            instruction = " ".join(instruction)

        short_term = self.redis.get(user_id, session_id)

        if instruction:
            vector = self.embedder.encode(instruction)
            long_term = self.search.search(vector, user_id)
        else:
            long_term = []

        long_term = self.filter.filter(long_term)

        memory = self.builder.build(short_term, long_term)

        payload["memory"] = memory

        return payload

    # =========================
    # UPDATE MEMORY
    # =========================
    def update(self, payload: dict, response: dict):

        user_id = payload["user_id"]
        session_id = payload["session_id"]

        instruction = payload["instruction"].get("raw", "")

        # 🔥 SAFETY
        if isinstance(instruction, list):
            instruction = " ".join(instruction)

        # ❌ SKIP EMPTY
        if not instruction or not instruction.strip():
            return

        # 🔥 CLEAN RESPONSE
        clean_response = {
            "summary": response.get("summary"),
            "status": response.get("status")
        }

        # 🔹 SHORT-TERM
        self.redis.save(user_id, session_id, {
            "instruction": instruction,
            "response": clean_response
        })

        # 🔹 FILTER RULE
        if len(instruction.split()) <= 2:
            return

        # 🔹 LONG-TERM
        vector = self.embedder.encode(instruction)

        self.faiss.add(vector, {
            "user_id": user_id,
            "text": instruction,
            "response": clean_response
        })

