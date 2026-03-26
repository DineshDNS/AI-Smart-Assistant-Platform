from app.services.cache.redis_client import RedisClient
from app.services.cache.cache_key_builder import build_cache_key
from app.services.cache.serializers import serialize, deserialize
from app.services.cache.config import CACHE_CONFIG


class CacheService:

    def __init__(self):
        self.client = RedisClient.get_client()

    def check_cache(self, normalized_data: dict, user_id: str = None):
        key = build_cache_key(normalized_data, user_id)

        cached_data = self.client.get(key)

        if cached_data:
            return {
                "cache_hit": True,
                "key": key,
                "data": deserialize(cached_data)
            }

        return {
            "cache_hit": False,
            "key": key
        }

    def store_cache(self, key: str, response: dict):
        self.client.setex(
            key,
            CACHE_CONFIG["ttl"],
            serialize(response)
        )