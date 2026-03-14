import os

def get_project_files(root_path: str):
    project_files = []

    for root, dirs, files in os.walk(root_path):
        for file in files:
            project_files.append({
                "path": os.path.join(root, file),
                "name": file,
                "extension": os.path.splitext(file)[1]
            })

    return project_files

def read_code_file(file_path: str, max_chars: int = 8000):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(max_chars)
        return content
    except Exception:
        return None

CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".java", ".cpp", ".c",
    ".html", ".css", ".json", ".md"
}

def is_code_file(extension: str):
    return extension.lower() in CODE_EXTENSIONS

import os

IGNORE_DIRS = {
    "venv",
    "node_modules",
    ".git",
    "__pycache__",
    ".idea",
    ".vscode",
    "dist",
    "build"
}

EXTENSION_LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".html": "HTML",
    ".css": "CSS",
    ".json": "JSON",
    ".md": "Markdown",
    ".yml": "YAML",
    ".yaml": "YAML"
}


def group_files_by_language(base_path: str):
    result = {}

    for root, dirs, files in os.walk(base_path):

        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            language = EXTENSION_LANGUAGE_MAP.get(ext)

            if not language:
                continue

            result.setdefault(language, []).append(
                os.path.join(root, file)
            )

    return result
