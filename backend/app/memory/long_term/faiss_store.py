import faiss
import numpy as np
import pickle
import os
from datetime import datetime, timedelta

from app.memory.config import FAISS_INDEX_PATH, LONG_TERM_TTL_DAYS


class FaissStore:

    def __init__(self, dim=384):
        self.dim = dim
        self.index_file = FAISS_INDEX_PATH + ".index"
        self.meta_file = FAISS_INDEX_PATH + ".pkl"

        if os.path.exists(self.index_file) and os.path.exists(self.meta_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.meta_file, "rb") as f:
                self.meta = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(dim)
            self.meta = []

    # =========================
    # ADD MEMORY
    # =========================
    def add(self, vector, data):
        """
        data must contain:
        user_id, text, response
        """

        entry = {
            "user_id": data["user_id"],
            "text": data["text"],
            "response": data["response"],
            "timestamp": datetime.utcnow().isoformat()
        }

        vec = np.array([vector]).astype("float32")

        self.index.add(vec)
        self.meta.append(entry)

        self._save()

    # =========================
    # SEARCH MEMORY
    # =========================
    def search(self, vector, user_id, k=5):
        if self.index.ntotal == 0:
            return []

        # 🔥 cleanup before search
        self._cleanup()

        vec = np.array([vector]).astype("float32")
        _, indices = self.index.search(vec, k * 2)  # extra for filtering

        results = []
        for i in indices[0]:
            if 0 <= i < len(self.meta):
                item = self.meta[i]

                # 🔥 USER FILTER
                if item["user_id"] == user_id:
                    results.append(item)

            if len(results) >= k:
                break

        return results

    # =========================
    # CLEANUP OLD DATA (TTL)
    # =========================
    def _cleanup(self):
        now = datetime.utcnow()

        valid_meta = []
        valid_vectors = []

        for i, meta in enumerate(self.meta):
            ts = datetime.fromisoformat(meta["timestamp"])

            if now - ts <= timedelta(days=LONG_TERM_TTL_DAYS):
                valid_meta.append(meta)

                # get vector from index
                vec = self.index.reconstruct(i)
                valid_vectors.append(vec)

        # 🔥 rebuild index
        self.index = faiss.IndexFlatL2(self.dim)

        if valid_vectors:
            vectors_np = np.array(valid_vectors).astype("float32")
            self.index.add(vectors_np)

        self.meta = valid_meta

        self._save()

    # =========================
    # SAVE TO DISK
    # =========================
    def _save(self):
        faiss.write_index(self.index, self.index_file)

        with open(self.meta_file, "wb") as f:
            pickle.dump(self.meta, f)

    # =========================
    # CLEAR ALL MEMORY
    # =========================
    def clear(self):
        self.index = faiss.IndexFlatL2(self.dim)
        self.meta = []
        self._save()