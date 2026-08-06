import os

import httpx
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
CHAT_ENDPOINT = "/api/chat/gemini"
HISTORY_LIMIT = 6


def request_gemini_reply(prompt: str, history: list[dict[str, str]]) -> dict:
    """Request an answer from the backend without exposing the Gemini key."""
    response = httpx.post(
        f"{API_BASE_URL}{CHAT_ENDPOINT}",
        json={"question": prompt, "messages": history},
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()


st.set_page_config(page_title="AI 챗봇", page_icon=":material/smart_toy:")
st.title("AI 챗봇")
st.caption("Gemini 응답은 안전한 FastAPI 백엔드를 통해 가져옵니다.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요. 무엇을 도와드릴까요?",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("메시지를 입력하세요", key="chat_input"):
    history = st.session_state.messages[-HISTORY_LIMIT:]
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Gemini가 답변을 생성하고 있습니다..."):
                result = request_gemini_reply(prompt, history)

            response = result["answer"]
            st.write(response)
            st.caption(
                f"provider={result['provider']} | model={result['model']}"
            )
        except httpx.ConnectError:
            response = (
                "백엔드에 연결할 수 없습니다. "
                "00_sample_backend의 FastAPI 서버가 실행 중인지 확인하세요."
            )
            st.error(response)
        except httpx.TimeoutException:
            response = "Gemini 응답 시간이 초과되었습니다. 잠시 후 다시 시도하세요."
            st.error(response)
        except httpx.HTTPStatusError as error:
            response = f"백엔드 API 오류가 발생했습니다. status={error.response.status_code}"
            st.error(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

if st.button("대화 초기화", icon=":material/delete_sweep:"):
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요. 무엇을 도와드릴까요?"}
    ]
    st.rerun()
