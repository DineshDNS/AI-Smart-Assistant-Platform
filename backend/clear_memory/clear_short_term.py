from app.services.cache.redis_client import RedisClient


def clear_short_term_memory():
    client = RedisClient.get_client()

    keys = client.keys("memory:*")

    if keys:
        client.delete(*keys)
        print(f"✅ Cleared {len(keys)} short-term memory keys")
    else:
        print("ℹ️ No short-term memory found")


if __name__ == "__main__":
    clear_short_term_memory()