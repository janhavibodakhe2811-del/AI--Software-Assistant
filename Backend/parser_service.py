"""
Parser Service — AST-based extraction of functions, classes,
imports, and API endpoints from Python and JavaScript/TypeScript files.
"""

import ast
import re
from typing import Optional


# ── Python AST Parser ────────────────────────────────────────────

def parse_python(content: str) -> dict:
    """
    Parse a Python file using the AST module.
    Returns functions, classes, imports, and decorators.
    """
    result = {
        "functions": [],
        "classes": [],
        "imports": [],
        "api_endpoints": [],
        "has_main": False,
    }

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return result

    for node in ast.walk(tree):
        # Top-level functions
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            fn_info = {"name": node.name, "args": [], "decorators": []}

            # Collect argument names
            for arg in node.args.args:
                fn_info["args"].append(arg.arg)

            # Collect decorators (useful for finding FastAPI routes)
            for dec in node.decorator_list:
                dec_str = ""
                if isinstance(dec, ast.Call):
                    if isinstance(dec.func, ast.Attribute):
                        dec_str = f"@{dec.func.attr}"
                    elif isinstance(dec.func, ast.Name):
                        dec_str = f"@{dec.func.id}"
                elif isinstance(dec, ast.Attribute):
                    dec_str = f"@{dec.attr}"
                elif isinstance(dec, ast.Name):
                    dec_str = f"@{dec.id}"

                if dec_str:
                    fn_info["decorators"].append(dec_str)

                    # Detect HTTP route decorators
                    if any(m in dec_str for m in ["get", "post", "put", "delete", "patch"]):
                        try:
                            path_arg = dec.args[0] if dec.args else None
                            if isinstance(path_arg, ast.Constant):
                                result["api_endpoints"].append({
                                    "method": dec_str.lstrip("@").upper(),
                                    "path": path_arg.value,
                                    "function": node.name,
                                })
                        except (AttributeError, IndexError):
                            pass

            result["functions"].append(fn_info)

        # Classes
        elif isinstance(node, ast.ClassDef):
            result["classes"].append(node.name)

        # Imports
        elif isinstance(node, ast.Import):
            for alias in node.names:
                result["imports"].append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                result["imports"].append(node.module)

        # Check for if __name__ == "__main__"
        elif isinstance(node, ast.If):
            try:
                if (isinstance(node.test, ast.Compare) and
                        isinstance(node.test.left, ast.Name) and
                        node.test.left.id == "__name__"):
                    result["has_main"] = True
            except AttributeError:
                pass

    return result


# ── JavaScript / TypeScript Regex Parser ─────────────────────────

def parse_javascript(content: str) -> dict:
    """
    Parse JS/TS files using regex patterns.
    Extracts functions, classes, imports, and Express/Next.js routes.
    """
    result = {
        "functions": [],
        "classes": [],
        "imports": [],
        "api_endpoints": [],
    }

    # Named functions
    fn_patterns = [
        r"function\s+(\w+)\s*\(",                          # function foo(
        r"const\s+(\w+)\s*=\s*(?:async\s*)?\(",            # const foo = (
        r"const\s+(\w+)\s*=\s*(?:async\s*)?\w+\s*=>",     # const foo = x =>
        r"(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s+(\w+)", # export function foo
    ]
    for pattern in fn_patterns:
        for match in re.finditer(pattern, content):
            name = match.group(1)
            if name not in result["functions"] and not name[0].isupper():
                result["functions"].append(name)

    # Classes
    for match in re.finditer(r"class\s+(\w+)", content):
        result["classes"].append(match.group(1))

    # ES6 imports
    for match in re.finditer(r"import\s+.*?from\s+['\"]([^'\"]+)['\"]", content):
        result["imports"].append(match.group(1))

    # Require imports
    for match in re.finditer(r"require\(['\"]([^'\"]+)['\"]\)", content):
        result["imports"].append(match.group(1))

    # Express routes
    route_pattern = r"(?:router|app)\.(get|post|put|delete|patch)\s*\(\s*['\"]([^'\"]+)['\"]"
    for match in re.finditer(route_pattern, content, re.IGNORECASE):
        result["api_endpoints"].append({
            "method": match.group(1).upper(),
            "path": match.group(2),
            "function": "anonymous",
        })

    # Next.js API route (export default handler)
    if "export default" in content and ("req" in content or "res" in content):
        result["api_endpoints"].append({
            "method": "HANDLER",
            "path": "(Next.js API route)",
            "function": "default",
        })

    return result


# ── Unified entry point ───────────────────────────────────────────

def parse_file(path: str, content: str, language: str) -> dict:
    """
    Parse a source file and return extracted info.
    Dispatches to the right parser based on language.
    """
    if language == "Python":
        parsed = parse_python(content)
    elif language in {"JavaScript", "TypeScript", "React/JSX", "React/TSX"}:
        parsed = parse_javascript(content)
    else:
        parsed = {"functions": [], "classes": [], "imports": [], "api_endpoints": []}

    # Build a flat list of symbol names for ModuleCard display
    symbols = (
        [f["name"] if isinstance(f, dict) else f for f in parsed.get("functions", [])] +
        parsed.get("classes", [])
    )

    return {
        "path": path,
        "language": language,
        "symbols": symbols[:20],           # cap at 20 for display
        "imports": parsed.get("imports", []),
        "api_endpoints": parsed.get("api_endpoints", []),
        "has_main": parsed.get("has_main", False),
        "line_count": content.count("\n") + 1,
    }


# ── Security pattern scanner ──────────────────────────────────────

SECURITY_PATTERNS = [
    {
        "pattern": r"(?:password|passwd|secret|api_key|apikey|token|private_key)\s*=\s*['\"][^'\"]{4,}['\"]",
        "title": "Hardcoded Secret / Credential",
        "severity": "high",
        "description": "A sensitive value appears to be hardcoded directly in source code.",
        "suggestion": "Move secrets to environment variables and use a .env file.",
    },
    {
        "pattern": r"eval\s*\(",
        "title": "Use of eval()",
        "severity": "high",
        "description": "eval() can execute arbitrary code and is a serious security risk.",
        "suggestion": "Avoid eval(). Use JSON.parse() or ast.literal_eval() as safe alternatives.",
    },
    {
        "pattern": r"exec\s*\(",
        "title": "Use of exec()",
        "severity": "medium",
        "description": "exec() executes dynamic code which may introduce vulnerabilities.",
        "suggestion": "Avoid exec() with untrusted input.",
    },
    {
        "pattern": r"subprocess\.(?:call|run|Popen)\s*\(.*shell\s*=\s*True",
        "title": "Shell Injection Risk",
        "severity": "high",
        "description": "Using shell=True with subprocess can allow command injection.",
        "suggestion": "Pass command as a list instead of a string, and avoid shell=True.",
    },
    {
        "pattern": r"(?:SELECT|INSERT|UPDATE|DELETE).*\+\s*(?:request|req|params|input|query)",
        "title": "Potential SQL Injection",
        "severity": "high",
        "description": "String concatenation in SQL queries can lead to SQL injection.",
        "suggestion": "Use parameterized queries or an ORM instead of string concatenation.",
    },
    {
        "pattern": r"(?:md5|sha1)\s*\(",
        "title": "Weak Hashing Algorithm",
        "severity": "medium",
        "description": "MD5 and SHA-1 are cryptographically broken and should not be used for security.",
        "suggestion": "Use bcrypt, argon2, or SHA-256+ for password hashing.",
    },
    {
        "pattern": r"TODO|FIXME|HACK|XXX",
        "title": "TODO / FIXME Comment",
        "severity": "low",
        "description": "Unresolved TODO or FIXME comment found.",
        "suggestion": "Review and resolve outstanding TODO items before production.",
    },
    {
        "pattern": r"console\.log\s*\(",
        "title": "Debug console.log()",
        "severity": "info",
        "description": "console.log() calls may expose sensitive data in production.",
        "suggestion": "Remove or replace with a proper logging library before production.",
    },
    {
        "pattern": r"print\s*\(",
        "title": "Debug print() statement",
        "severity": "info",
        "description": "print() statements may expose sensitive data in production.",
        "suggestion": "Replace with Python's logging module.",
    },
]


def scan_security(path: str, content: str) -> list[dict]:
    """Scan a file for security issues using regex patterns."""
    import re
    issues = []
    lines = content.split("\n")

    for rule in SECURITY_PATTERNS:
        for i, line in enumerate(lines, start=1):
            if re.search(rule["pattern"], line, re.IGNORECASE):
                issues.append({
                    "file": path,
                    "line": i,
                    "severity": rule["severity"],
                    "title": rule["title"],
                    "description": rule["description"],
                    "suggestion": rule["suggestion"],
                })
                break  # one issue per rule per file is enough

    return issues


# ── Performance pattern scanner ───────────────────────────────────

PERF_PATTERNS = [
    {
        "pattern": r"for\s+\w+\s+in\s+\w+.*:\s*\n.*\.append\(",
        "title": "List comprehension opportunity",
        "description": "A for-loop with .append() can often be replaced with a faster list comprehension.",
        "suggestion": "Consider using [x for x in iterable] instead of a loop with .append().",
    },
    {
        "pattern": r"time\.sleep\s*\(\s*[^0]\d*\s*\)",
        "title": "Blocking sleep() in async context",
        "description": "time.sleep() blocks the entire thread. In async code this halts other coroutines.",
        "suggestion": "Use asyncio.sleep() instead of time.sleep() in async functions.",
    },
    {
        "pattern": r"SELECT\s+\*\s+FROM",
        "title": "SELECT * query",
        "description": "Selecting all columns is inefficient and may expose unneeded data.",
        "suggestion": "Specify only the columns you need in your SELECT statement.",
    },
    {
        "pattern": r"import\s+\*",
        "title": "Wildcard import",
        "description": "Wildcard imports pollute the namespace and can slow down startup.",
        "suggestion": "Import only what you need: from module import specific_thing",
    },
    {
        "pattern": r"global\s+\w+",
        "title": "Use of global variable",
        "description": "Global variables can lead to hard-to-debug state issues.",
        "suggestion": "Consider encapsulating state in a class or passing it as parameters.",
    },
]


def scan_performance(path: str, content: str) -> list[dict]:
    """Scan a file for performance issues."""
    import re
    issues = []

    for rule in PERF_PATTERNS:
        if re.search(rule["pattern"], content, re.IGNORECASE | re.MULTILINE):
            issues.append({
                "file": path,
                "title": rule["title"],
                "description": rule["description"],
                "suggestion": rule["suggestion"],
            })

    return issues
