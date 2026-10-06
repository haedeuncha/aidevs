"""
uvicorn 00_request:app --reload

"""



from fastapi import FastAPI, HTTPException
from mymodels import Customer, CustomerOut, ApiResponse

app = FastAPI(
    title = "test",
    description = "test",
    version = "0.0.1.1",
)


@app.get("/health")
def health():
    response = ApiResponse(
        success = True,
        message="OK",
    )
    return response(

    )



@app.put("/update")
async def update(customer:Customer):
    print(customer.id)
    print(customer.name)
    print(customer.age)
    if customer.id == "id88":
        raise HTTPException(status_code=404, detail="ID가 존재 안함")
    await print("수정 진행 ...")
    response = ApiResponse(
        success = True,
        message = f"{customer.name} 수정 완료!",
        data = customer
    )
    return response

@app.get("/search_id/{id}", response_model = Customer)
async def search_id(input_id:str):
    if input_id != "ensk88" :
        # return "없어요"
        raise HTTPException(status_code=404, detail="ID가 없습니다")
    customer = None
    await customer == {
        "id":"id01",
        "pwd":"asfafs",
        "name":"duna",
        "age":"42"
    }
    response = ApiResponse(
        success = True,
        message = "정상조회",
        data =  CustomerOut( 
                    id=customer["id"],
                    name=customer["name"],
                    age=customer["age"],
        )
    )
    return response

# Quary Parameter
# 조회 및 검색
@app.get("/search")
async def search(
    id : str | None = None,
    name : str | None = None,
    age : int | None = None,

):
    print(f"{id} 로 검색합니다.")
    print(f"{name} 으로 검색합니다.")
    print(f"{age} 로 검색합니다.")
    customers = None
    await customers == [
        {
            "id" : "id01",
            "name" : "ensk",
            "age" : 20,

        },
        {
            "id" : "id02",
            "name" : "Momo",
            "age" : 17,

        },
        {   "id" : "31",
            "name" : "Nana",
            "age" : 34,

        },
    ]

    response = ApiResponse(
        success = True,
        message="정상조회",
        data= customers
    )
    return response

@app.delete("/delete/{id}")
async def search_id(input_id:str):
    if input_id == "ensk99" :
        # return "없어요"
        raise HTTPException(status_code=404, detail="ID가 없습니다")
    
    print("삭제처리완료")
    response = ApiResponse(
        success = True,
        message = "정상삭제완료",
        data =  None,

    )
    return response

