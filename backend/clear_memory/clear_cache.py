from app.services.cache.redis_client import RedisClient

def clear_all_cache():
    client = RedisClient.get_client()
    client.flushall()
    print("✅ Redis cache cleared successfully!")

if __name__ == "__main__":
    clear_all_cache()