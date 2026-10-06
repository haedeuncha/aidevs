"""
uvicorn 00_http:app --reload
"""

from fastapi import FastAPI
from dataclasses import dataclass

app = FastAPI(
    title="First FastAPI",
    description="FastAPI 서버가 어떻게 시작되는지 확인하는 첫 예제입니다.",
    version="0.0.1",
)

#Model
# 1.Memo
@dataclass
class Memo:
    id: int
    title: str
    content: str




#Mock data
memos = []
memos.append(Memo(
        id=100,
        title="졸려",
        content="뭐라는거지",
    ))

memos.append(Memo(
        id=200,
        title="졸려",
        content="뭐라는거지",
    ))

memos.append(Memo(
        id=300,
        title="졸려",
        content="뭐라는거지",
    ))




@app.get("/memo/get/{memo_id}")
def read_memo(memo_id: int) -> Memo :
    """
    read_memooooooooo
    """
    return Memo(
        id=100,
        title="졸려",
        content="뭐라는거지",
    )
    

@app.get("/memo/getback")
def read_back_memo():
    """
    getback
    """
    return

@app.post("/memo/create")
def create_memo(memo: Memo):
    """
    create memo
    """
    memos.append(memo)
    return

# 수정
@app.put("/memo/modify")
def modify_memo():
    """
    수정
    """
    return

# 삭제
@app.delete("/memo/remove")
def remove_memo():
    """
    삭제
    """
    return

