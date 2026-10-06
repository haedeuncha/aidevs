"""데이터베이스조회 탭입니다."""
import httpx
import streamlit as st
import pandas as pd

API_BASE_URL = "https://zero2-mini-choi.onrender.com"

@st.dialog("삭제")
def show_del(p:dict) -> None:
    st.info("Delete")
    st.write(f"{p['name']}삭제 하시겠습니까?")
    if st.button("삭제"):
        with st.spinner("삭제 요청"): 
            response = httpx.delete(f"{API_BASE_URL}/product/delete/{p['id']}", timeout=10.0)
        if response.status_code == 200:
            # 화면을 다시 출력한다.
            st.rerun()



@st.dialog("수정")
def show_up(p:dict) -> None:
    st.info(f"{p['id']}를 수정하겠습니다")
    with st.form(f"form_{p['id']}"):
        product_name = st.text_input("이름:", value=p["name"])
        product_price = st.number_input("가격:" ,value=int(p["price"]))
        if st.form_submit_button("수정"):
            payload = {"name":product_name,"price": product_price}
            with st.spinner("데이터 수정"): 
                response = httpx.put(f"{API_BASE_URL}/product/Update/{p['id']}",json= payload, timeout=10.0)
            if response.status_code == 200:
                st.rerun()


def product_select() -> None:
    """데이터를 확인합니다."""

    st.subheader("데이터베이스조회")
    st.caption("product 테이블을 선택하고 데이터를 확인합니다.")

    with st.spinner("데이터 요청"): 
        response = httpx.get(f"{API_BASE_URL}/product/getall", timeout=10.0)
    if response.status_code == 200:
        result = response.json()

        # df = pd.DataFrame(result)
        # st.dataframe(df)
        if not result:
            st.info("Product가 없습니다")
        for p in result:
            with st.container(border= True):
                product_col, button_col = st.columns([3,2])
                with product_col:
                    st.write(p["id"])
                    st.write(p["name"])
                    st.write(f"{p['price']}원")
                with button_col:
                    if st.button("삭제", key=f"del_{p['id']}"):
                        show_del(p)
                    if st.button("수정", key=f"up_{p['id']}"):
                        show_up(p)


    else:
        st.warning("Fail")
            
                    