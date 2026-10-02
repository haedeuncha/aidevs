from fastapi import FastAPI

app = FastAPI(title="Weather MCP Server")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "weather-mcp"}


@app.get("/mcp")
def get_weather() -> dict:
    return {
        "city": "Seoul",
        "temperature_c": 22,
        "condition": "clear",
        "unit": "C",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8010)
