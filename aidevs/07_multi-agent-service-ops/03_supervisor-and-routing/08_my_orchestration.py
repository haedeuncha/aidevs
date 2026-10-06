"""Lab 03-08: 파티 매칭 Supervisor Team.

시나리오:
    참가자 조건을 정리하고(profile) 파티 후보를 매칭한(matcher) 뒤 안전을 검토합니다(safety).
    조건이 부족하면 사용자에게 되묻고, 후보가 없거나 안전 이슈가 있으면 matcher를 한 번
    다시 실행할지 포기할지 Supervisor가 고릅니다.

학습 질문:
    고정 순서가 아니라 State에 따라 분기할 때, Supervisor의 선택을 어떻게 통제할 수 있을까요?

확인할 내용:
    Python이 State에서 허용되는 다음 행동의 집합을 계산하고, Supervisor(LLM)는 그 안에서만
    고릅니다. 허용 밖 선택, 최대 호출 수, matcher 재시도 횟수는 Python이 통제합니다.
"""

from shared.travel_contracts import LearningAgentResult, PartySupervisorDecision
from shared.travel_llm import run_with_metadata
from worker_registry import load_worker_registry


WORKERS = load_worker_registry()
MAX_MATCHER_RETRIES = 1
# matcher가 고를 수 있는 샘플 참가자 풀입니다. 풀에 없는 사람은 후보가 될 수 없습니다.
PARTICIPANT_POOL = [
    {"id": "U01", "nickname": "하늘", "area": "서울 강남", "available": "토요일 오후", "likes": ["보드게임", "전략"]},
    {"id": "U02", "nickname": "모카", "area": "서울 강남", "available": "토요일 오후", "likes": ["보드게임", "카드게임"]},
    {"id": "U03", "nickname": "도리", "area": "서울 서초", "available": "토요일 오후", "likes": ["보드게임"]},
    {"id": "U04", "nickname": "루나", "area": "서울 강남", "available": "일요일 저녁", "likes": ["방탈출", "보드게임"]},
    {"id": "U05", "nickname": "코코", "area": "서울 강남", "available": "토요일 오후", "likes": ["보드게임", "퍼즐"]},
    {"id": "U06", "nickname": "바다", "area": "경기 성남", "available": "토요일 오후", "likes": ["보드게임"]},
    {"id": "U07", "nickname": "별이", "area": "서울 강남", "available": "토요일 오후", "likes": ["파티게임", "보드게임"]},
    {"id": "U08", "nickname": "솔", "area": "부산", "available": "토요일 오후", "likes": ["보드게임"]},
]


def new_state() -> dict[str, object]:
    return {"last_agent": None, "outputs": {}, "matcher_runs": 0}


def allowed_next(state: dict[str, object]) -> list[str]:
    """현재 State에서 Supervisor가 고를 수 있는 다음 행동을 계산합니다."""
    last = state["last_agent"]
    if last is None:
        return ["profile_agent"]

    completed = state["outputs"][last]["completed"]
    can_retry = state["matcher_runs"] <= MAX_MATCHER_RETRIES
    retry_or_finish = ["matcher_agent", "finish"] if can_retry else ["finish"]

    if last == "profile_agent":
        return ["matcher_agent"] if completed else ["ask_user"]
    if last == "matcher_agent":
        return ["safety_agent"] if completed else retry_or_finish
    if last == "safety_agent":
        return ["finish"] if completed else retry_or_finish
    raise ValueError(f"알 수 없는 Agent입니다: {last}")


def final_status(state: dict[str, object], selected: str) -> tuple[str, str]:
    """종료 행동(ask_user·finish)을 status와 reason으로 바꿉니다."""
    if selected == "ask_user":
        return "needs_input", "missing_information"
    last = state["last_agent"]
    if state["outputs"][last]["completed"]:
        return "completed", "safety_passed"
    if last == "matcher_agent":
        return "no_match", "no_candidate_after_retry"
    return "rejected", "safety_failed_after_retry"


def supervisor_agent(request: str, state: dict[str, object], options: list[str]) -> dict:
    prompt = f"""당신은 supervisor_agent입니다. 직접 매칭·검토하지 마세요.
Worker: profile_agent(조건 정리), matcher_agent(후보 매칭), safety_agent(안전 검토)
현재 State: {state}
지금 고를 수 있는 다음 행동: {options}
후보가 없거나 안전 이슈가 있을 때 matcher_agent를 다시 부르면 조건을 완화해 재시도합니다.
재시도로 나아질 것 같으면 matcher_agent, 아니면 finish를 고르세요.
사용자 요청: {request}
PartySupervisorDecision 계약으로 반환하고 agent_id는 supervisor_agent로 작성하세요."""
    return run_with_metadata("openai", prompt, PartySupervisorDecision)


def selected_worker_agent(agent_id: str, request: str, outputs: dict[str, object]) -> dict:
    if agent_id not in WORKERS:
        raise ValueError(f"허용되지 않은 Worker입니다: {agent_id}")
    worker = WORKERS[agent_id]
    pool = f"\n참가자 풀(후보는 이 목록의 id에서만 고르세요): {PARTICIPANT_POOL}" if agent_id == "matcher_agent" else ""
    prompt = f"""당신은 {agent_id}입니다.
이름: {worker['name']}
Goal: {worker['goal']}
Instructions: {worker['instructions']}
사용자 요청: {request}
이전 Agent Context: {outputs}{pool}
LearningAgentResult 계약으로 반환하세요. 이전 Agent의 결과를 그대로 복사하지 말고 당신의 역할 결과만 작성하세요."""
    result = run_with_metadata(worker["provider"], prompt, LearningAgentResult)
    if result["result"] is not None:
        # Agent 정체성은 모델이 생성한 값이 아니라 오케스트레이터가 아는 값을 신뢰합니다.
        result["result"]["agent_id"] = agent_id
    return result


def party_team_agent(request: str, max_llm_calls: int = 12) -> dict[str, object]:
    state = new_state()
    trace: list[dict[str, object]] = []

    def log(actor: str, response: dict) -> None:
        trace.append({"step": len(trace) + 1, "actor": actor, "provider": response["provider_requested"], "model": response["model"], "result": response["result"], "error": response["error"]})

    while len(trace) < max_llm_calls:
        options = allowed_next(state)
        decision = supervisor_agent(request, state, options)
        log("supervisor_agent", decision)
        if decision["error"]:
            return {"status": "failed", "reason": "supervisor_failed", "state": state, "trace": trace}
        selected = decision["result"]["next_agent"]
        if selected not in options:
            return {"status": "blocked", "reason": "invalid_transition", "state": state, "trace": trace}
        if selected in {"ask_user", "finish"}:
            status, reason = final_status(state, selected)
            return {"status": status, "reason": reason, "state": state, "trace": trace}
        if len(trace) >= max_llm_calls:
            break

        worker = selected_worker_agent(selected, request, state["outputs"])
        log(selected, worker)
        if worker["error"]:
            return {"status": "failed", "reason": "worker_failed", "state": state, "trace": trace}
        state["last_agent"] = selected
        state["outputs"][selected] = worker["result"]
        if selected == "matcher_agent":
            state["matcher_runs"] += 1

    return {"status": "failed", "reason": "max_llm_calls", "state": state, "trace": trace}


if __name__ == "__main__":
    result = party_team_agent("이번 주 토요일 서울 강남에서 보드게임 파티 5명을 모집하고 싶어요. 시간은 오후12시입니다.")
    print(result)
    print("전체 상태:", result["status"])
    print("종료 이유:", result["reason"])
    for event in result["trace"]:
        print(event["step"], event["actor"], event["provider"], event["model"], "오류:", event["error"])
