"""
uvicorn 00_request:app --reload
"""


from fastapi import FastAPI, HTTPException
from mymodels import Customer, CustomerDetail


app = FastAPI(
    title = "Request Test",
    description = "request test",
    version = "0.1"
)


@app.get("/health")
def health():
    return {"msg":"OK"}

# Request Body
# insert, update
@app.post("/register")
def register(customer:Customer):
    print(customer.id)
    print(customer.name)
    print(customer.age)
    return {"msg":f"{customer.name} 가입축하!"}

# Path Paramter
# 127.0.0.1:8000/get/id01
# get , delete
@app.get("/get/{input_id}")
def get(input_id : str):
    if input_id != "id01":
        # return "없어요"
        raise HTTPException(status_code=404, detail="ID가 존재 안함")
    customer_detail = CustomerDetail(
        id = input_id,
        name = "james",
        age = 20
    )
    return {"data":customer_detail}


# Query Parameter
# 검색
@app.get("/search")
def search(
    id : str,
    name : str,
    age : int
):
    print(f"{id}로 검색 합니다.")
    print(f"{name}로 검색 합니다.")
    print(f"{age}로 검색 합니다.")
    
    return {"result":"검색 결과"}

