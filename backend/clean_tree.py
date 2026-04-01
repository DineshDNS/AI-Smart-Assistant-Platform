import os

# ❌ Ignore these (auto-generated / not manual)
EXCLUDE_DIRS = {
    "venv", "__pycache__", ".git", "node_modules",
    "Lib", "Include", "Scripts", "site-packages", "tmp"
}

EXCLUDE_EXT = {".pyc", ".pkl", ".index"}
EXCLUDE_FILES = {"faiss_index.index", "faiss_index.pkl"}

def is_valid(name, path):
    if name in EXCLUDE_DIRS:
        return False
    if name in EXCLUDE_FILES:
        return False
    if any(name.endswith(ext) for ext in EXCLUDE_EXT):
        return False
    return True

def generate_tree(path, prefix=""):
    items = sorted(os.listdir(path))
    for item in items:
        full_path = os.path.join(path, item)

        if not is_valid(item, full_path):
            continue

        print(prefix + "|-- " + item)

        if os.path.isdir(full_path):
            generate_tree(full_path, prefix + "|   ")

# Run from backend folder
generate_tree(".")