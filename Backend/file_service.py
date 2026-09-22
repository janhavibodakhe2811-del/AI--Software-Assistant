"""
File Service — builds a file tree and reads source files
from a cloned repository, respecting ignore patterns.
"""

import os
from pathlib import Path
from typing import Optional

from app.config import SUPPORTED_EXTENSIONS, IGNORE_PATTERNS, MAX_FILES
from app.models.schemas import FileNode


def _should_ignore(name: str) -> bool:
    """Return True if a file/folder should be skipped."""
    if name.startswith("."):
        # Keep .env.example etc., skip hidden dirs/files
        if name not in {".env.example", ".gitignore", ".dockerignore"}:
            return True
    return name in IGNORE_PATTERNS


def build_file_tree(root_path: str, rel_path: str = "") -> FileNode:
    """
    Recursively build a FileNode tree from the given directory.
    """
    abs_path = os.path.join(root_path, rel_path) if rel_path else root_path
    name = os.path.basename(abs_path) or os.path.basename(root_path)

    if os.path.isfile(abs_path):
        return FileNode(
            name=name,
            type="file",
            path=rel_path or name,
            size=os.path.getsize(abs_path),
        )

    children = []
    try:
        entries = sorted(os.listdir(abs_path))
    except PermissionError:
        entries = []

    for entry in entries:
        if _should_ignore(entry):
            continue
        child_rel = os.path.join(rel_path, entry) if rel_path else entry
        child_node = build_file_tree(root_path, child_rel)
        children.append(child_node)

    return FileNode(
        name=name,
        type="directory",
        path=rel_path or ".",
        children=children,
    )


def collect_source_files(root_path: str) -> list[dict]:
    """
    Walk the repo and collect all source files with their content.

    Returns list of dicts:
        { path, content, language, size }
    Limited to MAX_FILES to control LLM cost.
    """
    files = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Prune ignored directories in-place
        dirnames[:] = [
            d for d in dirnames
            if not _should_ignore(d)
        ]

        for fname in filenames:
            if _should_ignore(fname):
                continue

            ext = Path(fname).suffix.lower()
            if ext not in SUPPORTED_EXTENSIONS:
                continue

            abs_file = os.path.join(dirpath, fname)
            rel_file = os.path.relpath(abs_file, root_path).replace("\\", "/")

            try:
                size = os.path.getsize(abs_file)
                if size > 200 * 1024:   # skip files > 200KB (likely generated)
                    continue

                with open(abs_file, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                files.append({
                    "path": rel_file,
                    "content": content,
                    "language": _detect_language(ext),
                    "size": size,
                })

                if len(files) >= MAX_FILES:
                    return files

            except (OSError, PermissionError):
                continue

    return files


def _detect_language(ext: str) -> str:
    """Map file extension to language name."""
    mapping = {
        ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
        ".jsx": "React/JSX", ".tsx": "React/TSX", ".java": "Java",
        ".go": "Go", ".rb": "Ruby", ".php": "PHP", ".cs": "C#",
        ".cpp": "C++", ".c": "C", ".h": "C/C++ Header",
        ".rs": "Rust", ".swift": "Swift", ".html": "HTML",
        ".css": "CSS", ".scss": "SCSS", ".json": "JSON",
        ".yaml": "YAML", ".yml": "YAML", ".toml": "TOML",
        ".md": "Markdown", ".sh": "Shell",
    }
    return mapping.get(ext, "Unknown")


def count_files(root_path: str) -> int:
    """Count total source files in a repo."""
    return len(collect_source_files(root_path))
