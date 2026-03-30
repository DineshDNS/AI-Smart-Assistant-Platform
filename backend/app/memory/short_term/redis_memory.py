import redis
import json
from app.memory.config import REDIS_TTL


class RedisMemory:

    def __init__(self):
        self.client = redis.Redis(host="localhost", port=6379, decode_responses=True)

    def _key(self, user_id, session_id):
        return f"memory:{user_id}:{session_id}"

    def save(self, user_id, session_id, data):
        key = self._key(user_id, session_id)

        self.client.lpush(key, json.dumps(data))
        self.client.ltrim(key, 0, 9)  # keep last 10
        self.client.expire(key, REDIS_TTL)

    def get(self, user_id, session_id):
        key = self._key(user_id, session_id)

        items = self.client.lrange(key, 0, -1)
        return [json.loads(i) for i in items]