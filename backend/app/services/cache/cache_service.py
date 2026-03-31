
from app.services.cache.redis_client import RedisClient
from app.services.cache.cache_key_builder import build_cache_key
from app.services.cache.serializers import serialize, deserialize
from app.services.cache.config import CACHE_CONFIG


class CacheService:

    def __init__(self):
        self.client = RedisClient.get_client()

    # =========================
    # 🔹 NEW: CHECK CACHE BY KEY (PRIMARY METHOD)
    # =========================
    def check_cache_by_key(self, key: str):
        cached_data = self.client.get(key)

        if cached_data:
            return {
                "cache_hit": True,
                "key": key,
                "data": deserialize(cached_data)
            }

        return {
            "cache_hit": False,
            "key": key,
            "data": None
        }

    # =========================
    # 🔹 OLD METHOD (DEPRECATED — KEEP FOR SAFETY)
    # =========================
    def check_cache(self, normalized_data: dict, user_id: str = None):
        """
        Deprecated: uses raw normalized_data (not semantic)
        Kept for backward compatibility
        """
        key = build_cache_key(normalized_data, user_id=user_id)

        return self.check_cache_by_key(key)

    # =========================
    # 🔹 STORE CACHE
    # =========================
    def store_cache(self, key: str, response: dict):
        self.client.setex(
            key,
            CACHE_CONFIG["ttl"],
            serialize(response)
        )

    # =========================
    # 🔹 OPTIONAL: DELETE CACHE (DEBUG / TESTING)
    # =========================
    def delete_cache(self, key: str):
        self.client.delete(key)

    # =========================
    # 🔹 OPTIONAL: CLEAR ALL CACHE (DANGEROUS)
    # =========================
    def clear_all(self):
        self.client.flushdb()

