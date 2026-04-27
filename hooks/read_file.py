import os

def read_file_hook(inputs: dict) -> dict:
    file_path = inputs["file_path"]

    if not os.path.exists(file_path):
        raise RuntimeError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return {**inputs, "file_content": content}