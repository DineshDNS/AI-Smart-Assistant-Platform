from app.services.normalization.normalization_service import run_normalization


def test_normalization():
    sample_input = {
        "request_id": "123",
        "user_id": "user_001",
        "processed_data": {
            "text": {
                "cleaned": "summarize this: ai is powerful",
                "tokens": ["summarize", "ai"]
            }
        },
        "errors": []
    }

    result = run_normalization(sample_input)

    print("\n=== NORMALIZATION OUTPUT ===\n")
    print(result)


if __name__ == "__main__":
    test_normalization()