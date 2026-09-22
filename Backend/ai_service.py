"""
AI Service — wraps Google Gemini API (new google-genai SDK) for:
  - Project summary generation
  - Module explanation
  - Architecture diagram (Mermaid)
  - API doc generation
  - Q&A chat about the codebase
"""

import json
import re
import time
from typing import Optional

from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY


# Lazy client — initialized on first use
_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is not set. Add it to backend/.env")
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def _safe_generate(prompt: str, fallback: str = "") -> str:
    """
    Call Gemini with automatic retry on 429 rate-limit errors.
    Free tier: 15 requests/minute → we back off and retry up to 3 times.
    """
    if not GEMINI_API_KEY:
        return fallback or "[AI not configured — add GEMINI_API_KEY to backend/.env]"

    max_retries = 3
    wait_seconds = 20   # start with 20s wait on rate limit

    for attempt in range(max_retries):
        try:
            client = _get_client()
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=2048,
                ),
            )
            return response.text.strip() if response.text else (fallback or "")

        except Exception as e:
            err_str = str(e)
            # 429 rate limit — wait then retry
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                if attempt < max_retries - 1:
                    time.sleep(wait_seconds)
                    wait_seconds *= 2   # exponential backoff: 20s → 40s → 80s
                    continue
                else:
                    # All retries exhausted — return graceful fallback
                    return fallback or "[Rate limit reached. Please wait a minute and re-analyze.]"
            # Any other error — return fallback immediately
            return fallback or f"[AI error: {err_str[:120]}]"

    return fallback or ""


# ── Project Summary ───────────────────────────────────────────────

def generate_project_summary(repo_name: str, files: list[dict]) -> str:
    """Generate a 3–5 sentence project summary."""
    file_list = "\n".join(
        f"  - {f['path']} ({f['language']}, {f['size']} bytes)"
        for f in files[:60]
    )

    prompt = f"""You are an expert software engineer analyzing a GitHub repository.

Repository name: {repo_name}

Files in this repository:
{file_list}

Write a concise project summary (3-5 sentences) that explains:
1. What this project does
2. The main technology stack
3. The overall architecture pattern (e.g., MVC, microservices, monolith)

Be specific and technical. Do not use generic phrases like "this is a great project".
"""
    return _safe_generate(prompt, f"A software project named '{repo_name}'.")


# ── Module Explanation ────────────────────────────────────────────

def explain_module(path: str, content: str, language: str, symbols: list[str]) -> dict:
    """
    Ask Gemini to explain a single file/module.
    Returns { summary, type }.
    """
    truncated = content[:3000] + ("\n... (truncated)" if len(content) > 3000 else "")
    symbol_list = ", ".join(symbols[:10]) if symbols else "none detected"

    prompt = f"""You are analyzing a source code file. Provide a brief explanation.

File: {path}
Language: {language}
Key symbols: {symbol_list}

Source code:
```
{truncated}
```

Respond with valid JSON only (no markdown, no explanation outside JSON):
{{
  "summary": "1-2 sentence explanation of what this file does",
  "type": "one of: service, route, model, config, utility, component, test, unknown"
}}
"""
    raw = _safe_generate(prompt)

    try:
        cleaned = re.sub(r"```(?:json)?|```", "", raw).strip()
        data = json.loads(cleaned)
        return {
            "summary": data.get("summary", "No summary available."),
            "type": data.get("type", "unknown"),
        }
    except (json.JSONDecodeError, ValueError):
        return {
            "summary": raw[:200] if raw else "Could not generate summary.",
            "type": "unknown",
        }


# ── Architecture Diagram ──────────────────────────────────────────

def generate_architecture_diagram(repo_name: str, modules: list[dict]) -> str:
    """Generate a Mermaid.js graph diagram of the project architecture."""
    module_list = "\n".join(
        f"  - {m['path']} (type: {m.get('type', 'unknown')})"
        for m in modules[:30]
    )

    prompt = f"""Generate a Mermaid.js graph diagram for this project: {repo_name}

Modules:
{module_list}

Requirements:
- Use `graph TD` direction
- Group related modules logically (frontend, backend, database, etc.)
- Keep it clean and readable with max 15 nodes
- Use short node labels
- Return ONLY the raw Mermaid diagram code, nothing else

Example format:
graph TD
    A[Frontend] --> B[API Layer]
    B --> C[Database]
"""
    diagram = _safe_generate(prompt)

    if not diagram.strip().startswith("graph"):
        match = re.search(r"graph\s+\w+.*", diagram, re.DOTALL)
        if match:
            diagram = match.group(0)
        else:
            diagram = f"""graph TD
    A[{repo_name}] --> B[Source Files]
    B --> C[Services]
    B --> D[Models]
    B --> E[Routes]
    A --> F[Configuration]"""

    return diagram


# ── API Documentation ─────────────────────────────────────────────

def generate_api_docs(endpoints: list[dict]) -> Optional[str]:
    """Generate markdown API documentation from extracted endpoints."""
    if not endpoints:
        return None

    endpoints_text = "\n".join(
        f"  - {ep['method']} {ep['path']}  (function: {ep['function']})"
        for ep in endpoints[:30]
    )

    prompt = f"""Generate clean API documentation in Markdown format for these endpoints:

{endpoints_text}

Format each endpoint as:
### METHOD /path
- **Description**: What this endpoint does
- **Function**: function name
- **Expected Request**: brief description
- **Expected Response**: brief description

Keep descriptions concise and technical.
"""
    return _safe_generate(prompt)


# ── Q&A Chat ──────────────────────────────────────────────────────

def answer_question(question: str, repo_name: str, context_files: list[dict]) -> str:
    """Answer a natural language question about the codebase."""
    context_parts = []
    total_chars = 0
    max_chars = 12000

    for f in context_files:
        snippet = f"### {f['path']} ({f['language']})\n```\n{f['content'][:800]}\n```\n"
        if total_chars + len(snippet) > max_chars:
            break
        context_parts.append(snippet)
        total_chars += len(snippet)

    context = "\n".join(context_parts)

    prompt = f"""You are an expert software engineer who has fully analyzed the '{repo_name}' repository.

Below are excerpts from the codebase:

{context}

---
Question: {question}

Answer clearly and specifically, referencing file names and function names where relevant.
If the answer cannot be determined from the provided context, say so honestly.
"""
    return _safe_generate(prompt, "I couldn't find a relevant answer in the codebase context provided.")
