import streamlit as st

# 로그인화면
loginout = st.query_params.get("loginout","logout")



if "input_login_id" not in st.session_state:
    st.session_state.input_login_id = ""

if "input_login_pwd" not in st.session_state:
    st.session_state.input_login_pwd = ""

def reset():
    st.session_state.input_login_id = ""
    st.session_state.input_login_pwd = ""

if loginout == "logout":
    st.title("로그인하십시오.")
    with st.form("login_form"):
        input_id = st.text_input("ID입력", key= "input_login_id")
        input_pwd = st.text_input("비밀번호입력", type= "pwd", key= "input_login_pwd")
        submit_area, reset_area = st.columns(2)
        with submit_area:
            login_submit = st.form_submit_button("LOGIN")
        with reset_area:
            reset = st.form_submit_button("RESET", on_click=reset)
        if login_submit:
            if input_id == "id123" and input_pwd == "pwd123":
                st.query_params["loginout"] = "login"
                st.rerun()
            else:
                st.toast("로그인 실패")

else:
    st.title("로그인 완료\n설문을 작성하여 제출해주십시오.")
    

# 로그인 시 아래 다양한 컴포넌트를 이용한 설문지 작성 후 출력
if "survey_done" not in st.session_state:
    st.session_state["survey_done"] = False

if loginout == "login":
    if st.session_state["survey_done"]:
        st.success("설문조사가 완료되었습니다!")
# 설문 완료시 나타나는 화면
        result = st.session_state["survey_result"]

        st.write(f"나이: {result['number']}세")
        st.write(f"이름: {result['name']}")
        st.write(f"사는 지역: {result['place']}")
        st.write(f"반려동물: {','.join(result['pet'])}")
        st.write(f"자차 보유: {'있음'if result['car_owner']else '아니오'}")
        st.write(f"오늘의 행복도: {result['happiness']}")
    else:
        with st.form("survey_form"):
#           설문조사 폼
            number = st.number_input("나이", min_value=1,value=1)
            name = st.text_input("이름")
            place = st.selectbox("사는지역",["서울","인천","경기"])
            pet = st.multiselect(
            "반려동물 유무",
            ["고양이","강아지","없음"]
            )
            car_owner = st.checkbox("자차를 보유하고 있습니다.")
            happiness = st.slider(
            "오늘의 행복도",
            min_value=0,
            max_value=10,
            value=5
            )
            complete = st.form_submit_button("설문 완료")

        if complete:
            st.session_state["survey_result"] = {
                "number": number,
                "name": name,
                "place": place,
                "pet": pet,
                "car_owner": car_owner,
                "happiness": happiness,
            }
            st.session_state["survey_done"] = True
            st.rerun()

        

    
    