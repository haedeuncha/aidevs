# Plan — 도슨트 에이전트

박물관 관람객 안내 Agent 팀 프로젝트 계획 문서입니다. `agent-design.md`가 State/Node/Edge 구조를 담당한다면,
이 문서는 **세 사람이 동시에 작업해도 코드가 충돌하지 않도록** 폴더, 파일, 함수명, API 형태를 먼저 고정합니다.

## 프로젝트 이름

도슨트 에이전트 (Docent Agent)

## 해결하려는 문제

관람객이 전시장에서 스마트폰으로 질문하면, **소장품·전시 설명**은 근거 문서에서 찾아 답하고(RAG),
**실시간 정보**(관람시간, 잔여 좌석, 위치)는 Tool을 호출해 정확한 값으로 답합니다.
두 경로를 구분하지 못하면 없는 정보를 지어내거나, 바뀐 시간표를 그대로 말하는 문제가 생깁니다.

## 사용자 시나리오

1. 사용자가 자연어로 질문한다. (예: "모나리자를 그린 화가는 누구야?")
2. Agent는 근거 문서 검색이 필요한지(RAG), 실시간 조회가 필요한지(Tool) 판단한다.
3. RAG는 소장품 도록에서, Tool은 mock 백엔드에서 정보를 가져온다.
4. 결과를 검증하고, 부족하면 최대 2회 재시도한 뒤 출처와 함께 최종 답변을 보여준다.

| # | 사용자 요청 | 필요한 경로 | 사용 Tool / 문서 | 최종 결과 형태 |
| --- | --- | --- | --- | --- |
| 1 | "모나리자를 그린 화가는 누구고 어떤 화풍이야?" | RAG | 소장품 도록 PDF, 작품 설명 카드 | 근거 인용 + 출처 표시 |
| 2 | "오늘 3시 도슨트 투어 남은 자리 있어?" | TOOL | `check_tour_availability` | 잔여 좌석 수 + 예약 안내 |
| 3 | "인상주의 전시실이 어디야, 어떻게 가?" | TOOL | `find_room_route` | 현재 위치 기준 경로 |
| 4 | "이 표로 특별전도 볼 수 있어?" | TOOL | `lookup_ticket_scope` | 이용 가능 여부 안내 |
| 5 | "3시 투어 2명 예약해줘" | TOOL (승인 필요) | `reserve_tour_slot` | 예약 확정 번호 (사용자 확인 후 실행) |

## Agent 흐름 초안

```text
start
-> analyze_request        (요청 분석, route 결정: rag | tool | both)
-> retrieve_context        (route가 rag/both일 때 소장품 문서 검색)
-> execute_tool             (route가 tool/both일 때 Tool 호출)
-> validate_result          (근거·조회 결과가 충분한지 검증)
-> reflect_or_retry         (부족하면 analyze_request로, 최대 2회)
-> generate_answer          (출처 포함 최종 응답)
```

## Memory 사용 계획

- **Session Memory (Redis, TTL)**: 오늘 둘러본 전시실, 언어 선택 — 관람이 끝나면 사라져도 되는 상태.
- **Long-term Memory (PostgreSQL)**: 선호 전시 카테고리, 접근성 요구(휠체어, 오디오가이드 언어) — 사용자가 확인·삭제 가능.
- **RAG 사용 여부**: 사용함. 소장품 도록 PDF·작품 설명·관람 FAQ를 pgvector에 색인해 검색.

## 역할 분담

세 사람이 각자 다른 파일을 소유해 동시에 작업해도 충돌하지 않도록, 아래 **디렉터리 구조**의 소유 파일 기준으로 나눕니다.

| 이름 | 담당 영역 | 소유 파일 | Agent 흐름 담당 노드 |
| --- | --- | --- | --- |
| 최두나 | LangGraph 오케스트레이션 · 통합 | `backend/agent_state.py`, `backend/graph.py`, `frontend/app.py`, `presentation/final-presentation.md` | `analyze_request`, `validate_result`, `reflect_or_retry`, `generate_answer` |
| 손영민 | RAG · 문서 파이프라인 | `backend/rag.py`, `data/raw/*`, `docs/tool-spec.md`(RAG 부분) | `retrieve_context` |
| 이원민 | Tool · Memory · 평가 | `backend/tools.py`, `backend/memory.py`, `backend/mock_data.py`, `eval/scenarios.json` | `execute_tool`, `reserve_tour_slot` 승인 흐름 |

> 세 영역 모두 `agent_state.py`의 State 필드를 함께 읽고 씁니다. **State 필드를 새로 추가하거나 이름을 바꿀 때는
> 반드시 세 사람이 먼저 합의**하고, 이 문서의 [State 계약](#state-계약) 표를 함께 수정합니다.

---

## 디렉터리 구조

`team-template`를 그대로 확장합니다. 굵게 표시한 파일이 이번에 새로 추가하는 파일입니다.

```text
team-template/
├─ README.md
├─ docs/
│  ├─ plan.md                 ← 이 문서
│  ├─ agent-design.md         (State / Node / Edge 상세)
│  ├─ tool-spec.md            **NEW** Tool·RAG API 명세
│  └─ test-checklist.md
├─ data/
│  └─ raw/                    **NEW** 소장품 도록 PDF, 작품 설명 원본 (손영민)
├─ backend/
│  ├─ requirements.txt
│  ├─ agent_state.py          State 정의 (최두나)
│  ├─ graph.py                Node/Edge 조립, run_agent (최두나)
│  ├─ tools.py                Tool 함수 5종 (이원민)
│  ├─ memory.py               **NEW** 세션·장기 Memory (이원민)
│  ├─ mock_data.py            **NEW** 전시실/투어/티켓 mock (이원민)
│  └─ rag.py                  **NEW** chunk·색인·검색 (손영민)
├─ eval/
│  └─ scenarios.json          **NEW** 회귀 테스트 시나리오 (이원민)
├─ frontend/
│  └─ app.py                  Streamlit 데모 (최두나)
└─ presentation/
   └─ final-presentation.md   (최두나)
```

### 폴더·파일 이름 규칙

- 폴더/파일명은 `snake_case`, 역할을 나타내는 명사로 짓는다. (`rag.py`, `mock_data.py`)
- Mock/테스트 전용 데이터는 `mock_` 접두사를 붙인다.
- 원본 자료(PDF 등)는 코드와 섞지 않고 `data/raw/`에만 둔다.
- 문서(`docs/*.md`)는 코드가 아니라 계약이다 — 함수 시그니처를 바꾸면 코드와 같은 PR에서 문서도 같이 고친다.

---

## State 계약

`backend/agent_state.py`. 세 사람이 공통으로 읽고 쓰는 유일한 공유 객체이므로 필드를 임의로 늘리지 않습니다.

```python
class AgentState(TypedDict):
    user_request: str          # 사용자 원문 질문
    route: str                 # "rag" | "tool" | "both"
    retrieved_context: list[str]  # RAG 검색 결과 (근거 텍스트 + 출처)
    required_tool: str         # 이번 턴에 호출할 Tool 이름, 없으면 ""
    tool_result: str           # Tool 실행 결과 (문자열로 요약)
    visitor_profile: dict      # 장기 Memory에서 불러온 선호/접근성 정보
    error_count: int           # 재시도 횟수, 2 넘으면 안전 종료
    final_answer: str          # 출처 포함 최종 응답
```

---

## 공용 함수명 목록

| 파일 | 함수명 | 입력 → 출력 | 담당자 |
| --- | --- | --- | --- |
| `graph.py` | `analyze_request(state) -> dict` | `AgentState` → `{"route": ...}` | 최두나 |
| `graph.py` | `validate_result(state) -> dict` | `AgentState` → `{"error_count": ...}` | 최두나 |
| `graph.py` | `reflect_or_retry(state) -> dict` | `AgentState` → `{"route": ...}` (재질문 포함) | 최두나 |
| `graph.py` | `generate_answer(state) -> dict` | `AgentState` → `{"final_answer": ...}` | 최두나 |
| `graph.py` | `build_graph() -> CompiledGraph` | — | 최두나 |
| `graph.py` | `run_agent(user_request: str) -> AgentState` | 질문 → 최종 State | 최두나 |
| `rag.py` | `index_documents(pdf_path: str) -> int` | PDF 경로 → 색인된 chunk 수 | 손영민 |
| `rag.py` | `retrieve_context(query: str, top_k: int = 3) -> list[str]` | 질문 → 근거 텍스트 목록(출처 포함) | 손영민 |
| `tools.py` | `get_exhibit_hours(room_name: str) -> dict` | 전시실 이름 → 관람시간/휴관일 | 이원민 |
| `tools.py` | `check_tour_availability(tour_time: str) -> dict` | 투어 시각 → 잔여 좌석 | 이원민 |
| `tools.py` | `find_room_route(current: str, destination: str) -> dict` | 현재/목적지 → 경로, 소요시간 | 이원민 |
| `tools.py` | `lookup_ticket_scope(ticket_type: str) -> dict` | 티켓 유형 → 이용 가능 전시 목록 | 이원민 |
| `tools.py` | `reserve_tour_slot(tour_time: str, headcount: int) -> dict` | 투어 시각/인원 → 예약 번호 (승인 후 호출) | 이원민 |
| `memory.py` | `get_session_state(session_id: str) -> dict` | 세션 ID → 오늘 둘러본 전시실 등 | 이원민 |
| `memory.py` | `get_visitor_profile(user_id: str) -> dict` | 사용자 ID → 선호/접근성 정보 | 이원민 |

함수명은 **동사 + 목적어** 형태로 통일합니다. (`get_`, `check_`, `find_`, `lookup_`, `reserve_`, `retrieve_`, `index_`)

---

## API 명세 (Tool 호출 스키마)

`04_function-calling-and-tool-use/01_function-calling-basic`에서 배운 JSON Schema 형식을 그대로 사용합니다.
LLM에는 아래 5개 스키마를 tool 목록으로 전달합니다.

```json
[
  {
    "name": "get_exhibit_hours",
    "description": "전시실 이름으로 관람 시간과 휴관일을 조회합니다.",
    "input_schema": {
      "type": "object",
      "properties": {
        "room_name": { "type": "string", "description": "전시실 이름, 예: 인상주의관" }
      },
      "required": ["room_name"]
    }
  },
  {
    "name": "check_tour_availability",
    "description": "도슨트 투어 시각의 잔여 좌석을 조회합니다.",
    "input_schema": {
      "type": "object",
      "properties": {
        "tour_time": { "type": "string", "description": "HH:MM 형식 투어 시각" }
      },
      "required": ["tour_time"]
    }
  },
  {
    "name": "find_room_route",
    "description": "현재 위치에서 목적지 전시실까지 경로를 안내합니다.",
    "input_schema": {
      "type": "object",
      "properties": {
        "current": { "type": "string", "description": "현재 위치, 없으면 정문" },
        "destination": { "type": "string", "description": "목적지 전시실 이름" }
      },
      "required": ["destination"]
    }
  },
  {
    "name": "lookup_ticket_scope",
    "description": "티켓 유형으로 이용 가능한 전시 목록을 조회합니다.",
    "input_schema": {
      "type": "object",
      "properties": {
        "ticket_type": { "type": "string", "description": "예: 상설전, 통합권" }
      },
      "required": ["ticket_type"]
    }
  },
  {
    "name": "reserve_tour_slot",
    "description": "도슨트 투어를 예약합니다. 되돌리기 어려운 액션이므로 사용자 승인 후에만 호출합니다.",
    "input_schema": {
      "type": "object",
      "properties": {
        "tour_time": { "type": "string", "description": "HH:MM 형식 투어 시각" },
        "headcount": { "type": "integer", "description": "예약 인원", "minimum": 1 }
      },
      "required": ["tour_time", "headcount"]
    }
  }
]
```

### Tool 응답 형식과 실패 처리

| Tool | 성공 응답 예시 | 실패 상황 → 처리 |
| --- | --- | --- |
| `get_exhibit_hours` | `{"open": "09:00", "close": "18:00", "closed_days": ["월"]}` | 존재하지 않는 전시실 → 전시실 목록 재질문 |
| `check_tour_availability` | `{"remaining_seats": 4}` | 지난 시각 요청 → 다음 회차 제안 |
| `find_room_route` | `{"path": ["정문", "2층", "인상주의관"], "eta_min": 6}` | 위치 정보 없음 → 정문 기준 경로로 대체 |
| `lookup_ticket_scope` | `{"included_exhibits": ["상설전", "인상주의 특별전"]}` | 인식 불가 티켓 코드 → 매표소 안내 |
| `reserve_tour_slot` | `{"reservation_id": "T-0925-3"}` | 중복/정원 초과 → 기존 예약 안내 후 재확인 질문 |

### RAG 검색 응답 형식

```json
{
  "chunks": [
    { "text": "모나리자는 레오나르도 다 빈치가...", "source": "소장품도록.pdf", "page": 42, "score": 0.83 }
  ]
}
```

`retrieve_context()`는 위 `chunks` 배열을 `["{text} (출처: {source} p.{page})", ...]` 형태의 문자열 목록으로
변환해 `AgentState.retrieved_context`에 넣습니다. 근거가 하나도 없으면 빈 리스트를 반환하고,
`generate_answer`는 이 경우 "자료에서 확인할 수 없다"고 답합니다 — 지어내지 않습니다.

---

## 통합 규칙

- 세 사람 모두 자기 소유 파일 안에서만 함수를 추가/수정하고, `agent_state.py`의 필드 이름은 위 계약을 그대로 사용한다.
- 새 Tool이나 State 필드가 필요하면 이 문서를 먼저 고치고 PR에 링크한 뒤 구현한다.
- `graph.py`는 세 사람의 결과물을 잇는 파일이라 최두나가 소유하되, 새 노드가 필요하면 담당자가 먼저 이 문서의
  [Agent 흐름 초안](#agent-흐름-초안)에 추가하고 최두나에게 알린다.
- 합치기 전 `eval/scenarios.json`의 4개 시나리오를 각자 로컬에서 통과시키고 병합한다.

## 참고 자료 매핑

| 영역 | 과정 폴더 |
| --- | --- |
| RAG 인덱싱·검색 | `04_rag/02, 06, 09_01~09_04` |
| Tool 정의·안전 실행 | `03_tool-use`, `04_function-calling-and-tool-use/01~03` |
| LangGraph State/Node/Edge | `06_langgraph-workflow/01~07` |
| Memory (세션/장기) | `05_memory/05, 06, 09~11` |
| 예약 승인 흐름 | `07_human-approval-and-safety/04~06` |
| 회귀 평가 | `08_agent-evaluation-and-tracing/02~05` |
