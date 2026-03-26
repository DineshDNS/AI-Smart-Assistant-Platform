import json


def serialize(data: dict) -> str:
    return json.dumps(data)


def deserialize(data: str) -> dict:
    return json.loads(data)