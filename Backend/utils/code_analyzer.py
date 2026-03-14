import os

IMPORTANT_FILES = {
    "backend": ["main.py", "app.py", "server.py", "wsgi.py"],
    "frontend": ["index.html"],
    "config": ["requirements.txt", "package.json", "pyproject.toml"]
}

def analyze_codebase(base_path: str) -> dict:
    analysis = {
        "root_files": [],
        "folders": {},
        "detected_tech": set(),
        "important_files": []
    }

    for root, dirs, files in os.walk(base_path):
        depth = root.replace(base_path, "").count(os.sep)
        if depth > 2:
            continue 

        rel_path = os.path.relpath(root, base_path)

        analysis["folders"][rel_path] = files

        for file in files:
            analysis["root_files"].append(os.path.join(rel_path, file))

            
            if file.endswith(".py"):
                analysis["detected_tech"].add("Python")
            elif file.endswith(".js"):
                analysis["detected_tech"].add("JavaScript")
            elif file.endswith(".html"):
                analysis["detected_tech"].add("HTML")
            elif file.endswith(".css"):
                analysis["detected_tech"].add("CSS")

            
            for group in IMPORTANT_FILES.values():
                if file in group:
                    analysis["important_files"].append(os.path.join(rel_path, file))

    analysis["detected_tech"] = list(analysis["detected_tech"])
    return analysis
