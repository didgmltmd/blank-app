import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

# 경로 설정
OUTAGE_DIR = "./data/정전"

def power_outage_vs_supply_demand_dashboard():
    st.title("⚡ 정전건수 vs 수요 & 공급 불균형횟수 대시보드")

    # 기존 정전 데이터
    outage_data = {
        "연도": [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
        "정전건수": [4038, 3702, 3673, 3592, 3329, 3960, 3503, 3816]
    }
    df = pd.DataFrame(outage_data)

    # 더미데이터 생성 (50~400 범위)
    np.random.seed(42)
    dummy_base = np.random.randint(50, 400, size=len(df))

    # 정전건수의 약 5~10% 정도 유사성 일부 반영
    variation = np.random.uniform(0.05, 0.1, size=len(df))
    dummy_data = (dummy_base + (df["정전건수"] * variation)).astype(int)
    df["불균형횟수"] = dummy_data


    # ✅ 그래프
    fig = go.Figure()

    # 불균형횟수 (보조 Y축 X)
    fig.add_trace(go.Scatter(
        x=df["연도"], y=df["불균형횟수"],
        name="불균형횟수", mode="lines+markers", line=dict(color="royalblue")
    ))

    # 정전건수 (보조 Y축)
    fig.add_trace(go.Scatter(
        x=df["연도"], y=df["정전건수"],
        name="정전건수", mode="lines+markers", line=dict(color="tomato"),
        yaxis="y2"
    ))

    fig.update_layout(
        title="연도별 불균형횟수 vs 정전건수 (보조 Y축)",
        xaxis=dict(title="연도", tickmode="linear", dtick=1),
        yaxis=dict(title="불균형횟수", side="left"),
        yaxis2=dict(title="정전건수", overlaying="y", side="right"),
        legend_title="구분",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
