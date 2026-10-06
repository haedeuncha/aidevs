"""항공편 검색과 취소 규정 조회를 제공하는 교육용 stdio MCP Server입니다."""

from typing import Literal

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "tour",
    instructions="출발/도착 도시와 가격 조건으로 항공편을 검색하고 항공편별 취소 규정을 제공합니다.",
)

FLIGHTS = [
    {
        "flight_id": "tour-air-001",
        "airline": "투어항공",
        "flight_number": "TA502",
        "origin": "부산",
        "destination": "서울",
        "price": 55_000,
    },
    {
        "flight_id": "tour-air-002",
        "airline": "투어항공",
        "flight_number": "TA210",
        "origin": "부산",
        "destination": "서울",
        "price": 89_000,
    },
    {
        "flight_id": "tour-air-003",
        "airline": "투어항공",
        "flight_number": "TA815",
        "origin": "서울",
        "destination": "부산",
        "price": 62_000,
    },
]

CANCELLATION_POLICIES = {
    "tour-air-001": "출발 1일 전까지 취소하면 전액 환불합니다.",
    "tour-air-002": "출발 3시간 전까지 취소하면 수수료 없이 환불합니다.",
    "tour-air-003": "출발 2일 전까지 취소하면 전액 환불합니다.",
}


@mcp.tool()
def search_flights(
    origin: Literal["부산", "서울"],
    destination: Literal["부산", "서울"],
    max_price: int = 100_000,
) -> dict:
    """출발/도착 도시와 편도 최대 가격으로 항공편을 검색합니다."""
    if max_price < 1:
        raise ValueError("max_price는 1 이상이어야 합니다.")
    if origin == destination:
        raise ValueError("origin과 destination은 서로 달라야 합니다.")
    matches = [
        flight for flight in FLIGHTS
        if flight["origin"] == origin
        and flight["destination"] == destination
        and flight["price"] <= max_price
    ]
    return {"items": matches, "source": "lab-tour-flight-catalog"}


@mcp.tool()
def get_cancellation_policy(flight_id: str) -> dict:
    """항공편 검색 결과의 flight_id로 해당 항공편의 취소 규정을 조회합니다."""
    policy = CANCELLATION_POLICIES.get(flight_id)
    if policy is None:
        raise ValueError(f"존재하지 않는 flight_id입니다: {flight_id}")
    flight = next(flight for flight in FLIGHTS if flight["flight_id"] == flight_id)
    return {
        "flight_id": flight_id,
        "airline": flight["airline"],
        "flight_number": flight["flight_number"],
        "policy": policy,
        "source": "lab-tour-policy-service",
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
