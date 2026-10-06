"""
uvicorn main:app --reload

"""
 


from fastapi import FastAPI
from router.router_customer_cu import router_cu
from router.router_customer_rd import router_rd

app = FastAPI(
    title = "test",
    description = "test",
    version = "0.0.1.1",
)

app.include_router(router_cu)
app.include_router(router_rd)
