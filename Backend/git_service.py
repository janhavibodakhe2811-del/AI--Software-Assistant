"""
Git Service — clones a GitHub repo into temp_repos/<repo_id>
and verifies it's within size limits.
"""

import os
import shutil
import uuid
import re

# Load .env and set GIT_PYTHON_GIT_EXECUTABLE BEFORE importing git
from dotenv import load_dotenv
load_dotenv()
_git_exe = os.getenv("GIT_PYTHON_GIT_EXECUTABLE", "")
if _git_exe:
    os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = _git_exe

import git
from pathlib import Path

from app.config import TEMP_REPOS_DIR, MAX_REPO_SIZE_MB


def _sanitize_github_url(url: str) -> str:
    """Normalize a GitHub URL to https clone format."""
    url = url.strip().rstrip("/")
    # Remove .git suffix if present
    if url.endswith(".git"):
        url = url[:-4]
    # Validate it's a github.com URL
    pattern = r"^https?://github\.com/[\w\-\.]+/[\w\-\.]+$"
    if not re.match(pattern, url):
        raise ValueError(f"Invalid GitHub URL: {url}")
    return url + ".git"


def _get_dir_size_mb(path: str) -> float:
    """Return total size of a directory in MB."""
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                pass
    return total / (1024 * 1024)


def clone_repository(repo_url: str) -> dict:
    """
    Clone a GitHub repository and return metadata.

    Returns:
        dict with keys: repo_id, local_path, name, url
    Raises:
        ValueError for invalid URLs or oversized repos
        RuntimeError for clone failures
    """
    clean_url = _sanitize_github_url(repo_url)
    repo_name = clean_url.split("/")[-1].replace(".git", "")
    repo_id = f"{repo_name}-{uuid.uuid4().hex[:8]}"

    os.makedirs(TEMP_REPOS_DIR, exist_ok=True)
    local_path = os.path.join(TEMP_REPOS_DIR, repo_id)

    # Clean up if path already exists
    if os.path.exists(local_path):
        shutil.rmtree(local_path)

    try:
        git.Repo.clone_from(
            clean_url,
            local_path,
            depth=1,          # shallow clone — faster, no full history needed
            single_branch=True,
        )
    except git.exc.GitCommandError as e:
        raise RuntimeError(f"Failed to clone repository: {str(e)}")

    # Check repo size
    size_mb = _get_dir_size_mb(local_path)
    if size_mb > MAX_REPO_SIZE_MB:
        shutil.rmtree(local_path, ignore_errors=True)
        raise ValueError(
            f"Repository is too large ({size_mb:.1f} MB). "
            f"Maximum allowed is {MAX_REPO_SIZE_MB} MB."
        )

    return {
        "repo_id": repo_id,
        "local_path": local_path,
        "name": repo_name,
        "url": repo_url.rstrip("/"),
    }


def cleanup_repository(repo_id: str) -> bool:
    """Delete a cloned repository from disk."""
    local_path = os.path.join(TEMP_REPOS_DIR, repo_id)
    if os.path.exists(local_path):
        shutil.rmtree(local_path, ignore_errors=True)
        return True
    return False


def get_repo_path(repo_id: str) -> str | None:
    """Return local path of a cloned repo, or None if not found."""
    path = os.path.join(TEMP_REPOS_DIR, repo_id)
    return path if os.path.exists(path) else None
