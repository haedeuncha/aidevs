"""Open-Meteo 실시간 날씨를 보여주는 Streamlit 앱입니다."""

from __future__ import annotations

import json
from urllib.parse import urlencode
from urllib.request import urlopen

import streamlit as st


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
CITIES = {
    "서울": {"latitude": 37.5665, "longitude": 126.9780},
    "부산": {"latitude": 35.1796, "longitude": 129.0756},
    "제주": {"latitude": 33.4996, "longitude": 126.5312},
}


@st.cache_data(ttl=600, show_spinner=False)
def get_live_weather(city: str) -> dict:
    """Open-Meteo에서 현재 날씨와 오늘의 시간대별 예보를 가져옵니다."""
    location = CITIES[city]
    query = urlencode(
        {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
            "hourly": "temperature_2m,weather_code",
            "forecast_days": 1,
            "timezone": "Asia/Seoul",
        }
    )
    with urlopen(f"{OPEN_METEO_URL}?{query}", timeout=10) as response:
        data = json.load(response)

    noon_index = next(
        (index for index, time in enumerate(data["hourly"]["time"]) if time.endswith("T12:00")),
        0,
    )
    return {
        "updated_at": data["current"]["time"],
        "temperature": data["current"]["temperature_2m"],
        "apparent_temperature": data["current"]["apparent_temperature"],
        "humidity": data["current"]["relative_humidity_2m"],
        "wind_speed": data["current"]["wind_speed_10m"],
        "weather_code": data["current"]["weather_code"],
        "morning": {"temperature": data["hourly"]["temperature_2m"][0], "weather_code": data["hourly"]["weather_code"][0]},
        "afternoon": {"temperature": data["hourly"]["temperature_2m"][noon_index], "weather_code": data["hourly"]["weather_code"][noon_index]},
    }


def weather_info(code: int) -> tuple[str, str, str]:
    if code == 0:
        return "☀️", "맑음", "맑은 날씨입니다. 야외 활동 시 자외선 차단에 유의하세요."
    if code in (1, 2, 3):
        return "⛅", "구름 조금", "구름이 다소 끼는 날입니다. 외출 전 최신 예보를 확인하세요."
    if code in (45, 48):
        return "🌫️", "안개", "가시거리가 낮을 수 있습니다. 운전 시 안전거리를 확보하세요."
    if code in (51, 53, 55, 56, 57):
        return "🌦️", "이슬비", "약한 비가 내릴 수 있습니다. 우산을 준비하세요."
    if code in (61, 63, 65, 66, 67, 80, 81, 82):
        return "🌧️", "비", "비가 내리고 있습니다. 우산과 미끄럼에 유의하세요."
    if code in (71, 73, 75, 77, 85, 86):
        return "❄️", "눈", "눈이 내릴 수 있습니다. 보행과 차량 운전에 유의하세요."
    return "⛈️", "뇌우", "천둥·번개 가능성이 있습니다. 야외 활동을 피하세요."


st.set_page_config(page_title="날씨누리 | 동네예보", page_icon="☀️", layout="wide")
st.markdown(
    """
    <style>
      .stApp { background: #f3f6fa; }
      .block-container { max-width: 1120px; padding-top: 1.6rem; }
      .brand { font-size: 1.7rem; font-weight: 800; color: #102c60; letter-spacing: -.06em; }
      .service { color: #697689; font-size: .84rem; }
      .hero { padding: 1.8rem 2rem; color: #fff; background: linear-gradient(110deg, #0a559f, #157abf); }
      .hero-city { margin: 0; font-size: 1.25rem; font-weight: 700; }
      .hero-sub { color: #dcedff; margin: .45rem 0 0; }
      .hero-temp { font-size: 4rem; font-weight: 800; letter-spacing: -.08em; text-align: right; }
      .forecast-row { padding: .75rem 0; border-bottom: 1px solid #edf0f4; }
      div[data-testid="stMetric"] { padding: .9rem; border-right: 1px solid #e6ebf1; text-align: center; background: #fff; }
      div[data-testid="stMetricLabel"] { justify-content: center; color: #6d7787; }
      div[data-testid="stMetricValue"] { justify-content: center; color: #172f59; }
    </style>
    """,
    unsafe_allow_html=True,
)

brand, service = st.columns([4, 1])
brand.markdown('<div class="brand">☀️ 날씨누리</div>', unsafe_allow_html=True)
service.markdown('<div class="service">기상정보 · Open-Meteo</div>', unsafe_allow_html=True)
st.divider()
st.caption("홈 〉 날씨 〉 동네예보")
st.title("동네예보")

city = st.radio("지역 선택", list(CITIES), horizontal=True, label_visibility="visible")

try:
    weather = get_live_weather(city)
except Exception as error:
    st.error(f"Open-Meteo 날씨 정보를 가져오지 못했습니다: {error}")
    st.stop()

icon, condition, notice = weather_info(weather["weather_code"])
st.markdown(
    f'''<div class="hero"><div style="display:flex;align-items:center;gap:1.4rem">
      <div style="font-size:4.2rem">{icon}</div><div style="flex:1"><p class="hero-city">{city}</p>
      <p class="hero-sub">{condition} · {weather["updated_at"].replace("T", " ")} 기준</p></div>
      <div class="hero-temp">{round(weather["temperature"])}°</div></div></div>''',
    unsafe_allow_html=True,
)

st.subheader("현재 관측")
metric1, metric2, metric3 = st.columns(3)
metric1.metric("체감온도", f'{round(weather["apparent_temperature"])}°C')
metric2.metric("풍속", f'{weather["wind_speed"]} km/h')
metric3.metric("습도", f'{weather["humidity"]}%')

left, right = st.columns([3, 2], gap="large")
with left:
    st.subheader("오늘의 예보")
    morning_icon, morning_label, _ = weather_info(weather["morning"]["weather_code"])
    afternoon_icon, afternoon_label, _ = weather_info(weather["afternoon"]["weather_code"])
    st.markdown(f'<div class="forecast-row">오전　{morning_icon}　{morning_label}<span style="float:right;font-weight:700">{round(weather["morning"]["temperature"])}°</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="forecast-row">오후　{afternoon_icon}　{afternoon_label}<span style="float:right;font-weight:700">{round(weather["afternoon"]["temperature"])}°</span></div>', unsafe_allow_html=True)
with right:
    st.subheader("기상 안내")
    st.info(notice)

st.divider()
st.caption("날씨 데이터 제공: Open-Meteo · 데이터는 10분간 캐시됩니다.")
