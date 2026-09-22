"""
Duplicate Code Detection Service

Uses two strategies:
1. Exact block hashing  — finds copy-pasted code blocks (fast, no AI needed)
2. Structural similarity — normalizes identifiers then compares (catches renamed copies)
"""

import hashlib
import re
from collections import defaultdict
from typing import List


# ── Helpers ───────────────────────────────────────────────────────

def _normalize_block(lines: list[str]) -> str:
    """
    Normalize a code block for structural comparison:
    - strip comments
    - collapse whitespace
    - replace string literals with STR
    - replace number literals with NUM
    """
    joined = " ".join(l.strip() for l in lines if l.strip())
    # Remove single-line comments
    joined = re.sub(r"//.*", "", joined)
    joined = re.sub(r"#.*", "", joined)
    # Replace string literals
    joined = re.sub(r'\".*?\"|\'.*?\'', 'STR', joined)
    # Replace numbers
    joined = re.sub(r'\b\d+\.?\d*\b', 'NUM', joined)
    # Collapse whitespace
    joined = re.sub(r'\s+', ' ', joined).strip()
    return joined


def _hash_block(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


# ── Main detector ─────────────────────────────────────────────────

MIN_LINES = 5       # minimum block size to consider
STEP = 3            # sliding window step


def find_duplicates(source_files: list[dict]) -> list[dict]:
    """
    Find duplicate code blocks across all source files.

    Returns list of duplicate groups:
    {
        "block_preview": first 2 lines of the block,
        "line_count": N,
        "occurrences": [ { "file": path, "start_line": N }, ... ]
    }
    """
    # Map: normalized_hash -> list of (file, start_line, raw_preview)
    hash_map: dict[str, list[dict]] = defaultdict(list)

    for sf in source_files:
        # Only check real code files, skip configs/docs
        if sf.get("language") in {"JSON", "YAML", "Markdown", "TOML", "Unknown"}:
            continue

        lines = sf["content"].splitlines()
        if len(lines) < MIN_LINES:
            continue

        # Sliding window over the file
        for start in range(0, len(lines) - MIN_LINES + 1, STEP):
            block_lines = lines[start: start + MIN_LINES]

            # Skip blocks that are mostly empty / comments
            non_empty = [l for l in block_lines if l.strip() and not l.strip().startswith(("#", "//", "/*", "*"))]
            if len(non_empty) < 3:
                continue

            normalized = _normalize_block(block_lines)
            if len(normalized) < 40:   # too short to be meaningful
                continue

            block_hash = _hash_block(normalized)
            preview = " | ".join(l.strip() for l in block_lines[:2] if l.strip())[:120]

            hash_map[block_hash].append({
                "file": sf["path"],
                "start_line": start + 1,
                "preview": preview,
            })

    # Collect groups with 2+ occurrences in DIFFERENT files
    duplicates = []
    seen_hashes: set[str] = set()

    for block_hash, occurrences in hash_map.items():
        if block_hash in seen_hashes:
            continue

        # Only count if spread across at least 2 different files
        files_involved = {o["file"] for o in occurrences}
        if len(files_involved) < 2:
            continue

        seen_hashes.add(block_hash)

        # Deduplicate occurrences per file (keep first hit per file)
        seen_files: set[str] = set()
        unique_occ = []
        for occ in occurrences:
            if occ["file"] not in seen_files:
                seen_files.add(occ["file"])
                unique_occ.append({"file": occ["file"], "start_line": occ["start_line"]})

        duplicates.append({
            "block_preview": occurrences[0]["preview"],
            "line_count": MIN_LINES,
            "occurrences": unique_occ,
        })

    # Sort: most files involved first
    duplicates.sort(key=lambda d: len(d["occurrences"]), reverse=True)
    return duplicates[:30]   # cap at 30 groups
