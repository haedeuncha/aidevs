# Weather MCP Deployment Project

이 프로젝트는 GitHub Actions CI/CD와 Docker Compose 운영 흐름을 따라가는 최소 배포 예제입니다.

## 구성

- weather-mcp: 날씨 MCP 서버
- backend: FastAPI 백엔드
- frontend: Streamlit UI

## 실행

```bash
docker compose up --build
```

## 확인

- 백엔드: http://localhost:8000/health
- 프론트엔드: http://localhost:8501
- MCP: http://localhost:8010/health
