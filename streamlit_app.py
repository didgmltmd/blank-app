# streamlit_app.py
import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium

# 데이터 로드
df = pd.read_csv("jinju_cctv_20250513.csv", encoding="euc-kr")


# 지도 생성
m = folium.Map(location=[35.1799817, 128.1076213], zoom_start=13)

# 마커 추가
for 위도, 경도, 목적 in zip(df['위도'], df['경도'], df['목적']):
    folium.Marker(
        location=[위도, 경도],
        popup=folium.Popup(목적, parse_html=True, max_width=100)
    ).add_to(m)

# Streamlit에서 지도 표시
st.title("진주시 CCTV 지도")
st_folium(m, width=700, height=500)
