from app.services.cache.redis_client import RedisClient
from app.memory.long_term.faiss_store import FaissStore


def clear_all_memory():
    # 🔹 Clear Redis memory (short-term only)
    client = RedisClient.get_client()
    keys = client.keys("memory:*")

    if keys:
        client.delete(*keys)
        print(f"✅ Cleared {len(keys)} Redis memory keys")
    else:
        print("ℹ️ No Redis memory found")

    # 🔹 Clear FAISS memory
    store = FaissStore()
    store.clear()

    print("✅ Long-term memory cleared")


if __name__ == "__main__":
    clear_all_memory()