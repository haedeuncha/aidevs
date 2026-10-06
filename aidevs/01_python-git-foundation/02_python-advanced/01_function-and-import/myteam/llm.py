def build_chat_response(request_data: dict) -> dict:
    """질문 dict를 받아 응답 dict를 만듭니다.

    request_data 예시:
        {
            "user": "kim",
            "message": "FastAPI란?",
            "model": "practice-model"
        }
    """

    user = request_data.get("user", "anonymous")#["user"]
    message = request_data.get("message", "").strip()#["message"]
    model = request_data.get("model", "practice-model")#["model"]

    print("응답기다리는중....")
    print("응답을 받았습니다.")

    return {
        "user": user,
        "message": message,
        "model": model,
        "answer": f"{user}님, '{message}'에 대한 연습용 답변입니다.",
    }