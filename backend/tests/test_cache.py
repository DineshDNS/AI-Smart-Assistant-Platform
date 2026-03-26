from app.services.cache.cache_service import CacheService


def test_cache():
    cache = CacheService()

    normalized_data = {
        "instruction": {"text": "predict"},
        "data": [
            {"type": "text", "content": "sales increased"}
        ]
    }

    user_id = "user_123"

    result1 = cache.check_cache(normalized_data, user_id)
    print("First:", result1)

    key = result1["key"]

    response = {"result": "prediction done"}
    cache.store_cache(key, response)

    result2 = cache.check_cache(normalized_data, user_id)
    print("Second:", result2)