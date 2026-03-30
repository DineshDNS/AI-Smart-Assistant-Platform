ef test_memory():
    mm = MemoryManager()

    payload = {
        "user_id": "user_001",
        "session_id": "sess_123",
        "instruction": {"text": "Explain AI"}
    }

    print(mm.process(payload))