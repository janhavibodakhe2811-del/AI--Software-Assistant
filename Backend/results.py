from fastapi import APIRouter, HTTPException
from app.models.schemas import ResultsResponse, RepoListResponse, DeleteResponse
from app.services.analysis_service import (
    get_analysis_results,
    list_all_analyses,
    delete_analysis,
)

router = APIRouter()


@router.get("/results/{repo_id}", response_model=ResultsResponse)
async def get_results(repo_id: str):
    """
    GET /api/results/{repo_id}
    Returns the full analysis results for a repository.
    """
    data = get_analysis_results(repo_id)
    if data is None:
        raise HTTPException(status_code=404, detail=f"No analysis found for repo_id: {repo_id}")
    return data


@router.get("/repos", response_model=RepoListResponse)
async def list_repos():
    """
    GET /api/repos
    Returns a list of all analyzed repositories.
    """
    repos = list_all_analyses()
    return RepoListResponse(repos=repos)


@router.delete("/repos/{repo_id}", response_model=DeleteResponse)
async def delete_repo(repo_id: str):
    """
    DELETE /api/repos/{repo_id}
    Deletes the stored analysis for a repository.
    """
    deleted = delete_analysis(repo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"No analysis found for repo_id: {repo_id}")
    return DeleteResponse(message=f"Analysis for {repo_id} deleted successfully.")
