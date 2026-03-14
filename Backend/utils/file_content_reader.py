import os

MAX_FILE_SIZE = 200_000  # 200 KB per file (safe for LLMs)


def read_file_content(file_path: str) -> str | None:
    try:
        if not os.path.exists(file_path):
            return None

        if os.path.getsize(file_path) > MAX_FILE_SIZE:
            return None

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    except Exception:
        return None

def read_project_files(grouped_files: dict):
    """
    Input:
    {
      "Python": ["path1", "path2"],
      "HTML": ["path3"]
    }

    Output:
    {
      "Python": [
        {"path": "...", "content": "..."}
      ]
    }
    """
    result = {}

    for language, files in grouped_files.items():
        result[language] = []

        for path in files:
            content = read_file_content(path)
            if content:
                result[language].append({
                    "path": path,
                    "content": content
                })

    return result
