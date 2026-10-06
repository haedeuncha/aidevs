import streamlit as st

st.title("Pizza")
st.caption("나만의 피자를 만들어 보세요 🍕")

def init_state():
    if "pizza" not in st.session_state:
        st.session_state.pizza= ""  
    if "dow" not in st.session_state:
        st.session_state.dow = ""
    if "cheese" not in st.session_state:
        st.session_state.cheese = ""
    if "topping" not in st.session_state:
        st.session_state.topping= ""
    if "count" not in st.session_state:
        st.session_state.count= 0 
      
def clear_state():
    st.session_state["pizza"]=""
    st.session_state["dow"]=""
    st.session_state["cheese"]=""
    st.session_state["topping"]=""
    st.session_state["count"]=0

init_state()

def add():
    st.session_state.count = st.session_state.count + 1

def dec():
    if st.session_state.count == 0:
        return
    st.session_state.count = st.session_state.count - 1

def make_p1():
    st.toast("P1 피자를 만듭니다.")
    st.session_state.pizza = "pizza1"
    st.session_state.dow = "p1_dow"
    st.session_state.cheese = "p1_cheese"
    st.session_state.topping = "p1_topping"
def make_p2():
    st.toast("P2 피자를 만듭니다.")
    st.session_state.pizza = "pizza2"
    st.session_state.dow = "p2_dow"
    st.session_state.cheese = "p2_cheese"
    st.session_state.topping = "p2_topping"
def make_p3():
    st.toast("P3 피자를 만듭니다.")
    st.session_state.pizza = "pizza3"
    st.session_state.dow = "p3_dow"
    st.session_state.cheese = "p3_cheese"
    st.session_state.topping = "p3_topping"

st.title("Pizza")

if st.session_state.pizza != "":
    st.info(f"당신이 선택한 피자는: {st.session_state.pizza}")
    st.info(f"갯수: {st.session_state.count}")
    add_left,dec_right = st.columns(2)
    with add_left:
        st.button("추가", on_click= add, use_container_width= True)
    with dec_right:
        st.button("감소", on_click= dec, use_container_width= True)
p1, p2, p3 = st.columns(3)

with p1:
    p1_clicked = st.button("P1",on_click = make_p1)

with p2:
    p1_clicked = st.button("P2",on_click = make_p2)

with p3:
    p1_clicked = st.button("P3",on_click = make_p3)

with st.form("pizza_form"):
    quantity = st.number_input("수량", min_value=1, value=1)

    name = st.text_input("주문자 이름")

    request = st.text_area("요청 사항")

    size = st.selectbox("피자 크기", ["S", "M", "L"])

    toppings = st.multiselect(
        "추가 토핑",
        ["페퍼로니", "버섯", "올리브", "파인애플"]
    )

    extra_cheese = st.checkbox("치즈 추가")

    spicy_level = st.slider("매운맛", min_value=0, max_value=5, value=2)
    input_dow = st.text_input("도우 선택", key="dow")
    input_cheese = st.text_input("치즈 선택", key="cheese")
    input_topping = st.text_input("토핑선택", key="topping")

    def clear_state_count():
        st.session_state["count"]=0

    left_col, right_col = st.columns(2)
    with left_col:
        submit = st.form_submit_button("제출")   
    
    with right_col:
        reset = st.form_submit_button("초기화", on_click=clear_state)




if submit:
    st.subheader(f"당신이 선택한 피자는 {st.session_state.pizza}")
    st.caption("정말 맛있어 보이는 피자네요! 🍕")
    st.info(f"{input_dow}, {input_cheese}, {input_topping},{quantity},{toppings}")