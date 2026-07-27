# AI 개발 과정 README 요약

원본 위치의 `README.md` 314개를 이 폴더에 **원래의 폴더 구조 그대로 복사**했습니다. 원본은 변경하지 않았습니다.

## 전체 과정 흐름

```text
01 Python·Git 기초
→ 02 FastAPI·Supabase 백엔드
→ 03 Streamlit 프론트엔드
→ 04 Supabase AI 미니 프로젝트
→ 05 LLM Agent 오케스트레이션
→ 06 LLM Agent 미니 프로젝트
→ 07 멀티 에이전트 서비스 운영
→ 08 Auto Healing 멀티 에이전트 프로젝트
```

## 과정별 핵심 요약

| 과정 | 핵심 내용 |
| --- | --- |
| `00_course-guide` | 설치, 계정, 공통 오류 해결, 학습 지원 자료 |
| `01_python-git-foundation` | Python 문법·파일·테스트와 Git/GitHub 기초 |
| `02_supabase-ai-backend` | FastAPI, LLM API, Supabase DB·Auth·Redis를 활용한 백엔드 |
| `03_supabase-ai-frontend` | Streamlit UI, FastAPI API 연결, 로그인 상태, 챗봇 화면 |
| `04_supabase-ai-mini-project` | 로그·DB·Redis·SSE·대시보드를 연결하는 미니 프로젝트 |
| `05_llm-agent-orchestration` | 프롬프트, Tool Use, MCP, RAG, Memory, LangGraph |
| `06_llm-agent-mini-project` | 일정 조정 단일 Agent의 도구 호출·검증·자기 성찰 프로젝트 |
| `07_multi-agent-service-ops` | Docker, GitHub Actions, AWS, 보안, 관측성, Auto Healing 운영 |
| `08_multi-agent-service-mini-project` | 멀티 에이전트 기반 장애 감지·복구·검증 최종 프로젝트 |

## 빠르게 찾는 법

- 각 과정의 첫 화면: `01`~`08` 폴더 바로 아래 `README.md`
- 설치·실행 방법: 원본 과정 폴더의 `SETUP.md`
- 참고 개념: `00_references/README.md`
- 단계별 실습: `10_labs/README.md`
- 과제: `20_assignments/README.md`
- 통합·최종 프로젝트: `99_*` 폴더의 `README.md`

## 보안 주의

`.env`, API 키, AWS 키, 비밀번호는 README·채팅·GitHub에 기록하거나 올리지 않습니다.
