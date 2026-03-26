import redis
from app.services.cache.config import CACHE_CONFIG


class RedisClient:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = redis.Redis(
                host=CACHE_CONFIG["host"],
                port=CACHE_CONFIG["port"],
                db=CACHE_CONFIG["db"],
                decode_responses=True
            )
        return cls._client