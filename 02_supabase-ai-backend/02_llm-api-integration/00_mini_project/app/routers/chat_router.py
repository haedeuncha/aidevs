from fastapi import APIRouter
from app.schemes.chat_scheme import ChatRequest, ChatResponse

chat_router = APIRouter()

@chat_router.get("/chat/gemini")
def chat_gemini(chat_request:ChatRequest) -> ChatResponse:
    return 