from fastapi import APIRouter, HTTPException

from backend.schemas import ChatRequest
from backend.services.llm_service import (
    ask_nutrition_assistant
)

router = APIRouter(
    prefix="/api",
    tags=["AI Assistant"]
)


@router.post("/chat")
def chat(request: ChatRequest):

    try:

        answer = ask_nutrition_assistant(
            request.query,
            context_query=request.context_query,
            top_k=request.top_k
        )

        return {
            "query": request.query,
            "answer": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )