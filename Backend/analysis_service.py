"""
Analysis Service — orchestrates the full pipeline:
  clone → parse → AI analysis → store results
"""

import json
import os
import time
from datetime import datetime

from app.services.git_service import clone_repository
from app.services.file_service import build_file_tree, collect_source_files
from app.services.parser_service import parse_file, scan_security, scan_performance
from app.services.ai_service import (
    generate_project_summary,
    explain_module,
    generate_architecture_diagram,
    generate_api_docs,
)
from app.services.duplicate_service import find_duplicates
from app.config import TEMP_REPOS_DIR

# In-memory store for results (persisted to JSON for durability)
# In production you'd use a real DB; for college this is fine
_RESULTS_DIR = os.path.join(TEMP_REPOS_DIR, "_results")


def _results_path(repo_id: str) -> str:
    os.makedirs(_RESULTS_DIR, exist_ok=True)
    return os.path.join(_RESULTS_DIR, f"{repo_id}.json")


def _save_results(repo_id: str, data: dict):
    with open(_results_path(repo_id), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _load_results(repo_id: str) -> dict | None:
    path = _results_path(repo_id)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return json.load(f)


def run_full_analysis(repo_url: str) -> str:
    """
    Full pipeline: clone → parse → AI → save.
    Returns repo_id on success.
    Raises on failure.
    """
    # ── Step 1: Clone ─────────────────────────────────────────────
    clone_info = clone_repository(repo_url)
    repo_id = clone_info["repo_id"]
    local_path = clone_info["local_path"]
    repo_name = clone_info["name"]

    # ── Step 2: Build file tree ───────────────────────────────────
    file_tree = build_file_tree(local_path)

    # ── Step 3: Collect source files ─────────────────────────────
    source_files = collect_source_files(local_path)

    # ── Step 4: Static parsing (AST + regex) ─────────────────────
    parsed_files = []
    all_security_issues = []
    all_perf_issues = []
    all_endpoints = []

    for sf in source_files:
        parsed = parse_file(sf["path"], sf["content"], sf["language"])
        parsed_files.append({**sf, **parsed})

        # Security scan
        sec = scan_security(sf["path"], sf["content"])
        all_security_issues.extend(sec)

        # Performance scan
        perf = scan_performance(sf["path"], sf["content"])
        all_perf_issues.extend(perf)

        # Collect API endpoints
        all_endpoints.extend(parsed.get("api_endpoints", []))

    # ── Step 5: AI — project summary ─────────────────────────────
    project_summary = generate_project_summary(repo_name, source_files)

    # ── Step 6: AI — module explanations (top files only) ────────
    # Free tier = 15 req/min. We use: 1 summary + up to 8 modules + 1 diagram + 1 api_docs = ~11 calls max.
    # Prioritize actual source code files, skip docs/tests/configs
    important_files = [
        f for f in parsed_files
        if not any(skip in f["path"].lower() for skip in [
            "test", "spec", "migration", ".lock", "package",
            "readme", "changelog", "license", "docs/", ".md"
        ])
        and f.get("language") not in {"Markdown", "YAML", "TOML", "JSON", "Unknown"}
    ][:8]   # hard cap at 8 to stay within free-tier quota

    modules = []
    for i, pf in enumerate(important_files):
        explanation = explain_module(
            pf["path"], pf["content"], pf["language"], pf.get("symbols", [])
        )
        modules.append({
            "path": pf["path"],
            "language": pf["language"],
            "type": explanation["type"],
            "summary": explanation["summary"],
            "functions": pf.get("symbols", [])[:8],
        })
        # Pace requests: 1 call every 5 seconds = max 12/min, safely under the 15/min limit
        if i < len(important_files) - 1:
            time.sleep(5)

    # ── Step 7: AI — architecture diagram ────────────────────────
    time.sleep(5)   # pace between AI calls
    diagram = generate_architecture_diagram(repo_name, modules)

    # ── Step 8: AI — API documentation ───────────────────────────
    if all_endpoints:
        time.sleep(5)
    api_docs = generate_api_docs(all_endpoints) if all_endpoints else None

    # ── Step 8b: Duplicate code detection ────────────────────────
    duplicates = find_duplicates(source_files)

    # ── Step 9: Determine primary language ───────────────────────
    lang_counts: dict[str, int] = {}
    for sf in source_files:
        lang = sf["language"]
        lang_counts[lang] = lang_counts.get(lang, 0) + 1
    primary_language = max(lang_counts, key=lang_counts.get) if lang_counts else "Unknown"

    # ── Step 10: Assemble & persist results ──────────────────────
    results = {
        "repo_info": {
            "repo_id": repo_id,
            "name": repo_name,
            "url": repo_url,
            "file_count": len(source_files),
            "summary": project_summary,
            "primary_language": primary_language,
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": "completed",
        },
        "file_tree": file_tree.model_dump(),
        "modules": modules,
        "security_issues": all_security_issues[:50],     # cap at 50
        "performance_issues": all_perf_issues[:30],
        "duplicates": duplicates,
        "api_docs": api_docs,
        "diagram": diagram,
        # Store source files for chat Q&A
        "_source_files": [
            {"path": sf["path"], "content": sf["content"], "language": sf["language"]}
            for sf in source_files
        ],
    }

    _save_results(repo_id, results)
    return repo_id


def get_analysis_results(repo_id: str) -> dict | None:
    """Retrieve stored analysis results (without internal source files)."""
    data = _load_results(repo_id)
    if data is None:
        return None
    # Strip internal source files from public response
    public = {k: v for k, v in data.items() if not k.startswith("_")}
    return public


def get_source_files_for_chat(repo_id: str) -> list[dict]:
    """Return source files stored for Q&A context."""
    data = _load_results(repo_id)
    if data is None:
        return []
    return data.get("_source_files", [])


def list_all_analyses() -> list[dict]:
    """List all stored repo analyses."""
    os.makedirs(_RESULTS_DIR, exist_ok=True)
    repos = []
    for fname in os.listdir(_RESULTS_DIR):
        if fname.endswith(".json"):
            try:
                with open(os.path.join(_RESULTS_DIR, fname), "r", encoding="utf-8", errors="replace") as f:
                    data = json.load(f)
                info = data.get("repo_info", {})
                repos.append({
                    "repo_id": info.get("repo_id", fname[:-5]),
                    "name": info.get("name", "Unknown"),
                    "url": info.get("url", ""),
                    "file_count": info.get("file_count", 0),
                    "analyzed_at": info.get("analyzed_at", ""),
                    "status": info.get("status", "completed"),
                })
            except (json.JSONDecodeError, KeyError):
                continue
    return sorted(repos, key=lambda x: x["analyzed_at"], reverse=True)


def delete_analysis(repo_id: str) -> bool:
    """Delete stored analysis results."""
    path = _results_path(repo_id)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
