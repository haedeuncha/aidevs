import os

import httpx
from fastapi import FastAPI

app = FastAPI(title="Weather Backend")
WEATHER_MCP_URL = os.getenv("WEATHER_MCP_URL", "http://weather-mcp:8010/mcp")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "backend"}


@app.get("/weather")
async def get_weather() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_MCP_URL, timeout=10.0)
        response.raise_for_status()
        return {"source": "backend", **response.json()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
