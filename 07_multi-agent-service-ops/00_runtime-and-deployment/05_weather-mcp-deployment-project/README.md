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

## CI/CD (GitHub Actions)

워크플로: `.github/workflows/aws-server-deploy.yml` (이름: Weather MCP CI/CD)

```text
main push (이 폴더 변경) 또는 수동 실행
-> ci: 문법 검사 -> compose config -> build -> compose up 후 /health, /weather 확인
-> deploy: SSH로 AWS 서버에 폴더 업로드 -> docker compose up -d --build -> /health, /weather 확인
```

필요한 Repository secrets: `AWS_HOST`, `AWS_USER`, `AWS_SSH_PRIVATE_KEY`, `AWS_SSH_KNOWN_HOSTS`

서버 준비: Docker + Docker Compose 플러그인 설치, 보안 그룹에서 8000/8501 포트 허용
