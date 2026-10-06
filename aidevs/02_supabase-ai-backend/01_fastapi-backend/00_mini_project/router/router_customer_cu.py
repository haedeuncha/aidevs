"""
uvicorn router_customer_cu:app --reload

"""



from fastapi import APIRouter, HTTPException
# router/router_customer_cu.py
from scheme.model_common import ApiResponse
from scheme.model_customer import Customer
router_cu = APIRouter()



@router_cu.get("/health")
def health():
    response = ApiResponse(
        success = True,
        message="OK",
    )
    return response(

    )

@router_cu.post("/register")
def create_memo(customer:Customer):
    """
    register memo
    """
    customer.append(customer)

    return

@router_cu.put("/update")
async def update(customer:Customer):
    print(customer.id)
    print(customer.name)
    print(customer.age)
    if customer.id == "id88":
        raise HTTPException(status_code=404, detail="ID가 존재 안함")
    # await 
    print("수정 진행 ...")
    response = ApiResponse(
        success = True,
        message = f"{customer.name} 수정 완료!",
        data = customer
    )
    return response


@router_cu.delete("/delete/{id}")
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

