from app.services.preprocessing.preprocessing_service import run_preprocessing


def test_single_audio():
    input_data = {
        "request_id": "test_1",
        "user_id": "user_1",
        "session_id": "session_1",
        "data": {
            "audio": ["./tmp/sample.mp3"]
        }
    }

    result = run_preprocessing(input_data)

    print("\n=== SINGLE AUDIO TEST ===")
    print(result)


def test_text_and_audio():
    input_data = {
        "request_id": "test_2",
        "user_id": "user_1",
        "session_id": "session_1",
        "data": {
            "text": "summarize this audio",
            "audio": ["./tmp/sample.mp3"]
        }
    }

    result = run_preprocessing(input_data)

    print("\n=== TEXT + AUDIO TEST ===")
    print(result)


def test_multi_audio():
    input_data = {
        "request_id": "test_3",
        "user_id": "user_1",
        "session_id": "session_1",
        "data": {
            "audio": ["./tmp/a1.mp3", "./tmp/a2.mp3"]
        }
    }

    result = run_preprocessing(input_data)

    print("\n=== MULTI AUDIO TEST ===")
    print(result)


def test_invalid_audio():
    input_data = {
        "request_id": "test_4",
        "user_id": "user_1",
        "session_id": "session_1",
        "data": {
            "audio": ["./tmp/invalid.xyz"]
        }
    }

    result = run_preprocessing(input_data)

    print("\n=== INVALID AUDIO TEST ===")
    print(result)


def test_live_audio_chunks():
    input_data = {
        "request_id": "test_5",
        "user_id": "user_1",
        "session_id": "session_1",
        "data": {
            "audio": ["./tmp/chunk1.wav", "./tmp/chunk2.wav"]
        }
    }

    result = run_preprocessing(input_data)

    print("\n=== LIVE AUDIO (CHUNKS) TEST ===")
    print(result)


if __name__ == "__main__":
    test_single_audio()
    test_text_and_audio()
    test_multi_audio()
    test_invalid_audio()
    test_live_audio_chunks()