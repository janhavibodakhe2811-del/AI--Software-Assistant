from fastapi import APIRouter, HTTPException
from app.services.analysis_service import get_analysis_results

router = APIRouter()


@router.get("/filetree/{repo_id}")
async def get_file_tree(repo_id: str):
    """
    GET /api/filetree/{repo_id}
    Returns the file tree for a repository.
    """
    data = get_analysis_results(repo_id)
    if data is None:
        raise HTTPException(status_code=404, detail=f"No analysis found for repo_id: {repo_id}")
    return data.get("file_tree", {})
