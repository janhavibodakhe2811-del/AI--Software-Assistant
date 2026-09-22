from pydantic import BaseModel
from typing import Optional, List


# ── Request bodies ────────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    repo_url: str


class ChatRequest(BaseModel):
    message: str


# ── Sub-models ────────────────────────────────────────────────────

class FileNode(BaseModel):
    name: str
    type: str                          # "file" | "directory"
    path: str
    size: Optional[int] = None
    children: Optional[List["FileNode"]] = None


class ModuleInfo(BaseModel):
    path: str
    language: Optional[str] = None
    type: Optional[str] = None         # service|route|model|config|utility|component|test|unknown
    summary: str
    functions: Optional[List[str]] = []


class SecurityIssue(BaseModel):
    file: str
    line: Optional[int] = None
    severity: str                      # high | medium | low | info
    title: str
    description: str
    suggestion: Optional[str] = None


class PerformanceIssue(BaseModel):
    file: str
    line: Optional[int] = None
    title: str
    description: str
    suggestion: Optional[str] = None


class DuplicateOccurrence(BaseModel):
    file: str
    start_line: Optional[int] = None


class DuplicateGroup(BaseModel):
    block_preview: str
    line_count: int
    occurrences: List[DuplicateOccurrence]


class RepoInfo(BaseModel):
    repo_id: str
    name: str
    url: str
    file_count: int
    summary: Optional[str] = None
    primary_language: Optional[str] = None
    analyzed_at: str
    status: str = "completed"


# ── Response bodies ───────────────────────────────────────────────

class AnalyzeResponse(BaseModel):
    repo_id: str
    message: str = "Analysis complete"


class ResultsResponse(BaseModel):
    repo_info: RepoInfo
    file_tree: Optional[FileNode] = None
    modules: List[ModuleInfo] = []
    security_issues: List[SecurityIssue] = []
    performance_issues: List[PerformanceIssue] = []
    duplicates: List[DuplicateGroup] = []
    api_docs: Optional[str] = None
    diagram: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = []


class RepoListItem(BaseModel):
    repo_id: str
    name: str
    url: str
    file_count: int
    analyzed_at: str
    status: str


class RepoListResponse(BaseModel):
    repos: List[RepoListItem]


class DeleteResponse(BaseModel):
    message: str


# ── Rebuild all forward-reference models after all classes defined ─
FileNode.model_rebuild()
ResultsResponse.model_rebuild()
