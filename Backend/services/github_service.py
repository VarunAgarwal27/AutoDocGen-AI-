import os
import shutil
import subprocess
import uuid

BASE_CLONE_DIR = "temp/github_repos"

def clone_github_repo(repo_url: str) -> str:
    """
    Clones a GitHub repo and returns local path
    """
    if not repo_url.startswith("https://github.com/"):
        raise ValueError("Invalid GitHub URL")

    repo_id = str(uuid.uuid4())
    clone_path = os.path.join(BASE_CLONE_DIR, repo_id)

    os.makedirs(BASE_CLONE_DIR, exist_ok=True)

    try:
        subprocess.run(
            ["git", "clone", repo_url, clone_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        raise RuntimeError("Failed to clone repository")

    return clone_path


def cleanup_repo(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)
