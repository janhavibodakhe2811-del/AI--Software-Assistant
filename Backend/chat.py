from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.analysis_service import get_analysis_results, get_source_files_for_chat
from app.services.ai_service import answer_question

router = APIRouter()


@router.post("/chat/{repo_id}", response_model=ChatResponse)
async def chat_with_repo(repo_id: str, request: ChatRequest):
    """
    POST /api/chat/{repo_id}
    Answer a natural language question about the codebase.
    """
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # Get repo info
    results = get_analysis_results(repo_id)
    if results is None:
        raise HTTPException(status_code=404, detail=f"No analysis found for repo_id: {repo_id}")

    repo_name = results["repo_info"]["name"]

    # Get source files for context
    source_files = get_source_files_for_chat(repo_id)

    try:
        answer = answer_question(request.message.strip(), repo_name, source_files)
        return ChatResponse(answer=answer, sources=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate answer: {str(e)}")
