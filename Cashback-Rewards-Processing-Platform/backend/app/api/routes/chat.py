from fastapi import APIRouter
from app.schemas.chat import(ChatRequest, ChatResponse)
from app.ai.rag.rag_service import(answer_question)

router = APIRouter()

@router.post("/ask", response_model=ChatResponse)
def ask_question(request:ChatRequest):
    result = answer_question(request.question)
    
    return ChatResponse(answer=result["answer"], sources= result["sources"])
