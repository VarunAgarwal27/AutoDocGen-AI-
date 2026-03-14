import ast


def analyze_python_code(code: str):
    """
    Returns:
    {
      "functions": [],
      "classes": [],
      "imports": [],
      "routes": []
    }
    """
    tree = ast.parse(code)

    result = {
        "functions": [],
        "classes": [],
        "imports": [],
        "routes": []
    }

    for node in ast.walk(tree):

        # detect function in the uploaded project
        if isinstance(node, ast.FunctionDef):
            result["functions"].append(node.name)

            # Detect FastAPI routes
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call):
                    if hasattr(decorator.func, "attr"):
                        if decorator.func.attr in ["get", "post", "put", "delete"]:
                            result["routes"].append({
                                "method": decorator.func.attr.upper(),
                                "function": node.name
                            })

        # Detect classes in the uploaded project
        if isinstance(node, ast.ClassDef):
            result["classes"].append(node.name)

        # Detect all imports in the uploaded project
        if isinstance(node, ast.Import):
            for alias in node.names:
                result["imports"].append(alias.name)

        if isinstance(node, ast.ImportFrom):
            if node.module:
                result["imports"].append(node.module)

    return result

def analyze_project_files(project_files: dict):
    """
    Input: output of read_project_files()
    """
    analysis = {}

    for language, files in project_files.items():
        analysis[language] = []

        if language != "Python":
            continue  # only Python for now

        for file in files:
            try:
                structure = analyze_python_code(file["content"])
                analysis[language].append({
                    "path": file["path"],
                    "structure": structure
                })
            except Exception:
                continue

    return analysis
