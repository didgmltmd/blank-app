import os
import pandas as pd
import streamlit as st
import plotly.express as px

# 데이터 디렉토리
DATA_DIR = "./data/전력수요"

# CSV 안전하게 읽는 함수
def safe_read_csv(file_path):
    try:
        return pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding="euc-kr")  # 또는 "cp949"

# 대시보드
def power_demand_dashboard():
    st.title("⚡ 전력수요 대시보드")

    # 1️⃣ 지역별 시간대별 전력거래량
    st.header("지역별 시간대별 전력거래량 (2017~2023)")
    file_list = [f for f in os.listdir(DATA_DIR) if "한국전력거래소_지역별 시간대별 전력거래량" in f]
    file_list.sort()

    region_files = {f.split("_")[-1].split(".")[0]: os.path.join(DATA_DIR, f) for f in file_list}
    selected_year = st.selectbox("연도 선택", list(region_files.keys()))

    df = safe_read_csv(region_files[selected_year])

    # ✅ 컬럼명 정리 (공백 제거)
    df.columns = [col.strip() for col in df.columns]

    # ✅ 지역 목록
    regions = df["지역"].unique()
    selected_regions = st.multiselect("지역 선택", regions, default=[regions[0]])

    if selected_regions:
        # ✅ 선택된 지역만 필터링
        filtered_df = df[df["지역"].isin(selected_regions)]

        # ✅ 숫자형으로 변환 (문자열 -> float)
        filtered_df["전력거래량(MWh)"] = pd.to_numeric(filtered_df["전력거래량(MWh)"], errors="coerce").fillna(0)

        # ✅ 지역별 시간대별 평균 계산
        df_avg = filtered_df.groupby(["지역", "거래시간"], as_index=False)["전력거래량(MWh)"].mean()

        # ✅ 그래프 출력
        fig = px.line(df_avg, x="거래시간", y="전력거래량(MWh)",
                       color="지역", title="선택된 지역별 시간대별 평균 전력거래량",
                       markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("✅ 지역을 선택하면 그래프가 나타납니다.")
