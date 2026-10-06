"""원본 과제 파일과 분리한 게시판 애플리케이션입니다."""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="메모 보드")


class BoardCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=2000)


class BoardUpdate(BoardCreate):
    id: int = Field(ge=1)


boards = {
    1: {"id": 1, "title": "FastAPI 공부 정리", "content": "FastAPI의 주요 특징을 정리해보았습니다.\n\n- 비동기 지원으로 고성능 제공\n- 자동 문서화 (Swagger UI 제공)\n- 타입 힌트 기반 데이터 검증\n\n예제 프로젝트를 만들어서 복습해보자!"},
    2: {"id": 2, "title": "오늘 할 일 목록", "content": "- FastAPI 과제 마무리\n- API 테스트하기\n- 수업 내용 복습하기"},
    3: {"id": 3, "title": "아이디어 메모", "content": "간단한 메모를 저장하고 관리하는 게시판을 만들어 보자."},
}
next_board_id = 4


# 게시판 화면의 HTML, CSS, JavaScript를 모두 이 파일에 작성했습니다.
PAGE_HTML = """
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>메모 보드</title>
  <style>
    :root { --blue:#1468ed; --line:#d9dde5; --ink:#15171b; --muted:#747983; }
    * { box-sizing:border-box; }
    body { margin:0; min-width:760px; font-family:Arial,"Noto Sans KR",sans-serif; color:var(--ink); background:linear-gradient(135deg,#f8fafc,#eef5ff); }
    .page { max-width:1548px; margin:auto; padding:42px 48px 64px; }
    header { display:flex; justify-content:space-between; align-items:center; margin-bottom:28px; }
    h1 { margin:0; font-size:40px; letter-spacing:-2px; }
    .clock { display:flex; gap:54px; align-items:center; padding:20px 28px; background:#fff; border-radius:13px; box-shadow:0 3px 12px #0002; font-size:24px; font-weight:700; }
    #clock { color:#1476ed; font-size:29px; }
    .layout { display:grid; grid-template-columns:435px 1fr; gap:38px; }
    .panel { background:#fff; border-radius:14px; box-shadow:0 2px 10px #0002; }
    .list-panel { min-height:616px; padding:30px; }
    h2 { margin:0 0 26px; font-size:28px; }
    #board-list { display:grid; gap:20px; }
    .board-item { display:grid; width:100%; grid-template-columns:44px 1fr 20px; gap:16px; align-items:center; padding:20px; border:1px solid var(--line); border-radius:11px; background:#fff; text-align:left; cursor:pointer; color:inherit; }
    .board-item:hover { background:#f8fbff; border-color:#9abcfb; }
    .board-item.selected { border:2px solid var(--blue); padding:19px; color:#075cdf; background:#f3f8ff; }
    .note-icon { width:31px; height:39px; border:3px solid currentColor; border-radius:4px; position:relative; }
    .note-icon:after { content:""; position:absolute; top:11px; left:6px; right:6px; height:3px; background:currentColor; box-shadow:0 8px currentColor; }
    .item-title { display:block; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:20px; font-weight:700; }
    .item-date { display:block; margin-top:7px; color:var(--muted); font-size:15px; }
    .arrow { font-size:38px; line-height:1; }
    .editor { min-height:616px; overflow:hidden; }
    .editor-body { padding:34px 38px 20px; }
    label { display:block; margin-bottom:11px; font-size:18px; font-weight:700; }
    input, textarea { width:100%; border:1px solid #ccd1d9; border-radius:8px; padding:15px; font:inherit; font-size:20px; outline:none; }
    input { height:57px; margin-bottom:30px; } textarea { min-height:307px; line-height:1.65; resize:vertical; }
    input:focus, textarea:focus { border:2px solid var(--blue); padding:14px; }
    .actions { display:flex; justify-content:flex-end; gap:22px; padding:19px 32px; border-top:1px solid #e8e8e8; }
    .action { min-width:145px; padding:15px 22px; border:0; border-radius:10px; color:#fff; font-size:21px; font-weight:700; cursor:pointer; }
    #new { color:var(--blue); border:2px solid var(--blue); background:#fff; } #save { background:var(--blue); } #delete { background:#ef3034; }
    .empty { text-align:center; color:var(--muted); }
    @media (max-width:950px) { .page{padding:28px}.layout{grid-template-columns:1fr}.clock{gap:20px} }
  </style>
</head>
<body>
  <main class="page">
    <header><h1>메모 보드</h1><div class="clock"><span>시계추가</span><span id="clock"></span></div></header>
    <section class="layout">
      <aside class="panel list-panel"><h2>기록된 메모들</h2><div id="board-list"></div></aside>
      <section class="panel editor">
        <div class="editor-body"><label for="title">제목</label><input id="title" placeholder="제목을 입력하세요"><label for="content">내용</label><textarea id="content" placeholder="내용을 입력하세요"></textarea></div>
        <div class="actions"><button class="action" id="new">새 글</button><button class="action" id="save">저장하기</button><button class="action" id="delete">삭제</button></div>
      </section>
    </section>
  </main>
  <script>
    const list=document.querySelector('#board-list'), title=document.querySelector('#title'), content=document.querySelector('#content');
    let selectedId=null, boards=[];
    function escapeHtml(text){const e=document.createElement('div');e.textContent=text;return e.innerHTML}
    function updateClock(){document.querySelector('#clock').textContent=new Date().toLocaleTimeString('en-GB')}
    function dateText(){return new Date().toLocaleString('ko-KR',{year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hour12:false})}
    function render(){list.innerHTML='';if(!boards.length){list.innerHTML='<p class="empty">작성된 메모가 없습니다.</p>';return}boards.forEach(b=>{const el=document.createElement('button');el.className='board-item '+(b.id===selectedId?'selected':'');el.innerHTML='<span class="note-icon"></span><span><span class="item-title">'+escapeHtml(b.title)+'</span><span class="item-date">'+dateText()+'</span></span><span class="arrow">›</span>';el.onclick=()=>selectBoard(b.id);list.append(el)})}
    async function load(){const r=await fetch('/borads/list');boards=(await r.json()).data;if(selectedId&&!boards.some(b=>b.id===selectedId))selectedId=null;if(selectedId)await selectBoard(selectedId);else if(boards.length)await selectBoard(boards[0].id);else clear()}
    async function selectBoard(id){const r=await fetch('/borads/'+id);if(!r.ok)return;const b=(await r.json()).data;selectedId=b.id;title.value=b.title;content.value=b.content;document.querySelector('#save').textContent='수정하기';document.querySelector('#delete').style.display='block';render()}
    function clear(){selectedId=null;title.value='';content.value='';document.querySelector('#save').textContent='등록하기';document.querySelector('#delete').style.display='none';render();title.focus()}
    async function save(){const body={title:title.value.trim(),content:content.value.trim()};if(!body.title||!body.content){alert('제목과 내용을 모두 입력해주세요.');return}let url='/borads/create',method='POST';if(selectedId){url='/borads';method='PUT';body.id=selectedId}const r=await fetch(url,{method,headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});if(!r.ok){alert('저장에 실패했습니다.');return}selectedId=(await r.json()).data.id;await load()}
    async function remove(){if(!selectedId||!confirm('이 메모를 삭제할까요?'))return;const r=await fetch('/borads/'+selectedId,{method:'DELETE'});if(r.ok){selectedId=null;await load()}}
    document.querySelector('#new').onclick=clear;document.querySelector('#save').onclick=save;document.querySelector('#delete').onclick=remove;updateClock();setInterval(updateClock,1000);load();
  </script>
</body>
</html>
"""


@app.get("/", include_in_schema=False)
def board_page():
    return HTMLResponse(PAGE_HTML)


@app.get("/borads/list")
def list_boards():
    return {"data": list(boards.values())}


@app.get("/borads/{board_id}")
def get_board(board_id: int):
    board = boards.get(board_id)
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return {"data": board}


@app.post("/borads/create", status_code=201)
def create_board(board: BoardCreate):
    global next_board_id
    new_board = {"id": next_board_id, "title": board.title, "content": board.content}
    boards[next_board_id] = new_board
    next_board_id += 1
    return {"message": "board created", "data": new_board}


@app.put("/borads")
def update_board(board: BoardUpdate):
    if board.id not in boards:
        raise HTTPException(status_code=404, detail="Board not found")
    boards[board.id] = {"id": board.id, "title": board.title, "content": board.content}
    return {"message": "board updated", "data": boards[board.id]}


@app.delete("/borads/{board_id}")
def delete_board(board_id: int):
    board = boards.pop(board_id, None)
    if board is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return {"message": "board deleted", "data": board}
