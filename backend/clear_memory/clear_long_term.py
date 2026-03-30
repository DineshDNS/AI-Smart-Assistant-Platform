from app.memory.long_term.faiss_store import FaissStore


def clear_long_term_memory():
    store = FaissStore()

    store.clear()

    print("✅ Long-term memory (FAISS) cleared successfully!")


if __name__ == "__main__":
    clear_long_term_memory()