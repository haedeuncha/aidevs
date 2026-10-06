# llm과 연동하는 service
import os

from app.core import chat_config  # noqa: F401
from app.schemes.ChatRequest import ChatRequest, ChatResponse
from google import genai


def call_gemini(chat_request: ChatRequest) -> ChatResponse:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다. .env 파일을 확인하세요.")

    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model,
        contents=chat_request.prompt,
    )
    return ChatResponse(answer=response.text)