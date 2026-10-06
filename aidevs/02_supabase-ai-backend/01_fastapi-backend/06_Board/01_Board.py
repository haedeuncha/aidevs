from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="보드확인")


class MemoCreate(BaseModel):
    id: int = Field(ge=1)
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)


class MemoUpdate(BaseModel):
    id: int = Field(ge=1)
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)


borads = {1: {"id": 1.0, "title": "FastAPI 시작", "content": "Swagger UI를 확인해봅시다."}}
next_board_id = 2


@app.get("/borads/list")
def list_board():
    return {"data": list(borads.values())}


@app.get("/borads/{memo_id}")
def get_memo(memo_id: int):
    borad = borads.get(memo_id)
    if borad is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return {"data": borad}


@app.post("/borads/create", status_code=201)
def create_memo(borad: MemoCreate):
    global next_board_id
    new_borad = {"id": next_board_id, "title": borad.title, "content": borad.content}
    borads[next_board_id] = new_borad
    next_board_id += 1
    return {"message": "borad created", "data": new_borad}


@app.put("/borads")
def update_borad(borad: MemoUpdate):
    if borad.id not in borads:
        raise HTTPException(status_code=404, detail="borad not found")
    borads[borad.id] = {"id": borad.id, "title": borad.title, "content": borad.content}
    return {"message": "borad updated", "data": borads[borad.id]}


@app.delete("/borads/{memo_id}")
def delete_memo(memo_id: int):
    if memo_id not in borads:
        raise HTTPException(status_code=404, detail="Memo not found")
    return {"message": "memo deleted", "data": borads.pop(memo_id)}
