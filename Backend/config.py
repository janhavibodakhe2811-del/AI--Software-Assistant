import os
from dotenv import load_dotenv

load_dotenv()

# Set git executable path before gitpython is used anywhere
_git_path = os.getenv("GIT_PYTHON_GIT_EXECUTABLE", "")
if _git_path:
    os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = _git_path

GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
TEMP_REPOS_DIR: str = os.getenv("TEMP_REPOS_DIR", "./temp_repos")
MAX_REPO_SIZE_MB: int = int(os.getenv("MAX_REPO_SIZE_MB", "100"))
MAX_FILES: int = int(os.getenv("MAX_FILES", "150"))

# File extensions we care about for analysis
SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".java", ".go", ".rb", ".php", ".cs",
    ".cpp", ".c", ".h", ".rs", ".swift",
    ".html", ".css", ".scss",
    ".json", ".yaml", ".yml", ".toml",
    ".md", ".txt", ".env.example",
    ".sh", ".dockerfile",
}

# Files/dirs to skip always
IGNORE_PATTERNS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    "env", ".env", "dist", "build", ".next", ".nuxt",
    "coverage", ".pytest_cache", ".mypy_cache",
    "*.lock", "*.log", "*.min.js", "*.min.css",
}
