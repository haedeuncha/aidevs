"""Chat 탭입니다."""
import httpx
import streamlit as st

from frontend_common import require_login

API_BASE_URL = "https://zero2-mini-choi.onrender.com"

def render_product() -> None:
    """로그인 후 mock 대화를 입력하고 누적 표시합니다."""

    st.subheader("Chat")
    st.caption("mock대화를 입력하십시오")

    with st.form("product_form", clear_on_submit=True):
        message = st.text_input("메시지 입력", placeholder="오늘 배운 내용을 정리해줘.")
        submitted = st.form_submit_button("전송")

    if submitted:

        message = message.strip()
        payload = {"product_id": "id01", "prompt": message}
        with st.spinner("전송 후 기다립니다."):
            response = httpx.post(f"{API_BASE_URL}/api/message", json=payload, timeout=5.0)
        if response.status_code == 200:
            result = response.json()
            st.info(message)
            st.info(result["answer"])
        else:
            st.warning("오류")