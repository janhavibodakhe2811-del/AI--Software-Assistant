from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.analysis_service import run_full_analysis

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_repository(request: AnalyzeRequest):
    """
    POST /api/analyze
    Clones a GitHub repo and runs full AI analysis.
    Returns the repo_id to fetch results.
    """
    if not request.repo_url or "github.com" not in request.repo_url:
        raise HTTPException(status_code=400, detail="Please provide a valid GitHub repository URL.")

    try:
        repo_id = run_full_analysis(request.repo_url)
        return AnalyzeResponse(repo_id=repo_id, message="Analysis complete")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error during analysis: {str(e)}")
