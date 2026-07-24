
import streamlit as st


st.set_page_config(page_title="로그인 설문", page_icon="📝")


def sign_in(user_id: str, password: str) -> bool:
    """학습용 로그인 검증: admin / 1234만 로그인할 수 있습니다."""
    return user_id == "admin" and password == "1234"


if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "survey_submitted" not in st.session_state:
    st.session_state.survey_submitted = False


if not st.session_state.is_logged_in:
    st.title("🔐 로그인")
    st.caption("학습용 계정: ID `admin` / 비밀번호 `1234`")

    with st.form("login_form"):
        user_id = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        login_clicked = st.form_submit_button("로그인")

    if login_clicked:
        if sign_in(user_id, password):
            st.session_state.is_logged_in = True
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호가 올바르지 않습니다. 다시 로그인해 주세요.")

else:
    st.title("📝 만족도 설문")

    if not st.session_state.survey_submitted:
        with st.form("survey_form"):
            age = st.number_input("나이", min_value=1, max_value=120, value=20)
            name = st.text_input("이름")
            opinion = st.text_area("서비스에 바라는 점")
            job = st.selectbox("직업", ["학생", "직장인", "자영업", "기타"])
            interests = st.multiselect(
                "관심 있는 주제 (한 가지만 선택)",
                ["AI", "데이터 분석", "웹 개발", "디자인", "창업"],
                max_selections=1,
            )
            agree = st.checkbox("개인정보 수집·이용에 동의합니다.")
            score = st.slider("서비스 만족도", min_value=1, max_value=10, value=5)
            submitted = st.form_submit_button("설문 제출")

        if submitted:
            if not name.strip():
                st.warning("이름을 입력해 주세요.")
            elif not agree:
                st.warning("개인정보 수집·이용 동의가 필요합니다.")
            else:
                st.session_state.survey_result = {
                    "이름": name,
                    "나이": age,
                    "직업": job,
                    "관심 주제": interests[0] if interests else "선택 안 함",
                    "서비스 만족도": f"{score} / 10",
                    "의견": opinion or "작성 안 함",
                }
                st.session_state.survey_submitted = True
                st.rerun()
    else:
        st.success("설문조사가 끝났습니다.")
        st.subheader("설문 결과지")
        st.table(
            [
                {"항목": key, "응답": value}
                for key, value in st.session_state.survey_result.items()
            ]
        )
        st.info("결과지 출력이 완료되었습니다.")
        st.stop()
