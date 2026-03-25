import pandas as pd


def convert_numpy(obj):
    """Convert numpy types to Python native"""
    if hasattr(obj, "item"):
        return obj.item()
    return obj


def make_json_safe(data):
    """Recursively clean data"""
    if isinstance(data, dict):
        return {k: make_json_safe(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [make_json_safe(v) for v in data]
    else:
        return convert_numpy(data)


def load_tabular(path: str) -> dict:
    if path.endswith(".csv"):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)

    preview = df.head(5).to_dict(orient="records")

    # FIX: clean preview
    safe_preview = make_json_safe(preview)

    return {
        "columns": df.columns.tolist(),
        "shape": list(df.shape),
        "preview": safe_preview
        # REMOVED "_dataframe"
    }