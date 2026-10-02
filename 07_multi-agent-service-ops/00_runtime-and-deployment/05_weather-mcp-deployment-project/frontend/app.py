import os

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.title("Weather Dashboard")

if st.button("Fetch weather"):
    try:
        response = requests.get(f"{BACKEND_URL}/weather", timeout=10)
        response.raise_for_status()
        data = response.json()
        st.write(data)
    except Exception as exc:
        st.error(f"Failed to fetch weather: {exc}")
