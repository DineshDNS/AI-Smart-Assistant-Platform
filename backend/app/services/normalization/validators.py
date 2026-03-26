def validate_preprocessing_output(data: dict):
    if not isinstance(data, dict):
        raise ValueError("Invalid input: not a dictionary")

    if "processed_data" not in data:
        raise ValueError("Missing processed_data")

    if not isinstance(data["processed_data"], dict):
        raise ValueError("processed_data must be a dictionary")