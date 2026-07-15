"""
uvicorn 00_http:app --reload
"""

from fastapi import FastAPI

app = FastAPI(
    title="First FastAPI",
    description="FastAPI 서버가 어떻게 시작되는지 확인하는 첫 예제입니다.",
    version="0.0.1",
)

@app.get("/get")
def read_memo():
    """  read_memo  """
    return 

@app.get("/getall")
def read_all_memo():
    """ read_all_memo """
    return 

@app.post("/create")
def create_memo():
    """ create_memo """
    return 

@app.put("/modify")
def modify_memo():
    """ modify_memo """
    return 

@app.delete("/remove")
def remove_memo():
    """ remove_memo """
    return 



