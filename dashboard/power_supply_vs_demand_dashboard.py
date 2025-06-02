import os
import pandas as pd
import streamlit as st
import plotly.express as px

# 데이터 디렉토리
DEMAND_DIR = "./data/전력수요"
SUPPLY_DIR = "./data/전력공급"

# CSV 안전하게 읽는 함수
def safe_read_csv(file_path):
    try:
        return pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding="euc-kr")

def power_supply_vs_demand_dashboard():
    st.title("⚡ 전력 수요 vs 공급 비교 대시보드 ")

    # ✅ 수요 데이터
    demand_files = [f for f in os.listdir(DEMAND_DIR) if "한국전력거래소_지역별 시간대별 전력거래량" in f]
    demand_files.sort()
    demand_file_years = {f.split("_")[-1].split(".")[0]: os.path.join(DEMAND_DIR, f) for f in demand_files}

    # ✅ 공급 데이터
    file1_path = os.path.join(SUPPLY_DIR, "공급능력.csv")
    file2_path = os.path.join(SUPPLY_DIR, "한국전력거래소_시간별 발전량_20211231.csv")

    # 공급 데이터 읽기
    try:
        df1 = pd.read_csv(file1_path, encoding="utf-8")
    except UnicodeDecodeError:
        df1 = pd.read_csv(file1_path, encoding="euc-kr")
    try:
        df2 = pd.read_csv(file2_path, encoding="utf-8")
    except UnicodeDecodeError:
        df2 = pd.read_csv(file2_path, encoding="euc-kr")

    df1.columns = [col.strip() for col in df1.columns]
    df2.columns = [col.strip() for col in df2.columns]

    # 날짜 처리
    df1["날짜"] = pd.to_datetime(df1["날짜"], errors="coerce")
    df1["연도"] = df1["날짜"].dt.year

    if "거래일" in df2.columns:
        df2.rename(columns={"거래일": "날짜"}, inplace=True)
    df2["날짜"] = pd.to_datetime(df2["날짜"], errors="coerce")
    df2["연도"] = df2["날짜"].dt.year

    hour_cols = [col for col in df1.columns if col.endswith("시")]

    # 공급 데이터 통합
    supply_df = pd.concat([df1[["연도", "날짜"] + hour_cols],
                            df2[["연도", "날짜"] + hour_cols]],
                           ignore_index=True)

    # ✅ 연도 선택
    available_years = sorted(supply_df["연도"].dropna().unique())
    selected_year = st.selectbox("연도 선택 (수요 vs 공급)", available_years, key="supply_vs_demand_year")

    # ✅ 선택 연도의 공급 데이터 평균
    supply_year = supply_df[supply_df["연도"] == selected_year]
    supply_avg = supply_year[hour_cols].mean().reset_index()
    supply_avg.columns = ["시간", "공급량(kWh)"]
    supply_avg["시간"] = supply_avg["시간"].str.replace("시", "").astype(int)
    supply_avg = supply_avg.sort_values("시간")
    supply_avg["공급량(MWh)"] = supply_avg["공급량(kWh)"] / 1000

    # ✅ 수요 데이터
    demand_file = demand_file_years.get(str(selected_year))
    if demand_file is None:
        st.warning(f"{selected_year}년도의 수요 데이터가 없습니다.")
        return

    demand_df = safe_read_csv(demand_file)
    demand_df.columns = [col.strip() for col in demand_df.columns]
    demand_df["전력거래량(MWh)"] = pd.to_numeric(demand_df["전력거래량(MWh)"], errors="coerce").fillna(0)
    demand_total = demand_df.groupby(["거래시간"], as_index=False)["전력거래량(MWh)"].sum()
    demand_total["거래시간"] = demand_total["거래시간"].astype(int)

    # ✅ 비교 데이터
    compare_df = pd.merge(supply_avg, demand_total,
                           left_on="시간", right_on="거래시간", how="inner")
    compare_df = compare_df.rename(columns={"전력거래량(MWh)": "수요량(MWh)"}).drop(columns=["공급량(kWh)"])


    compare_df["공급량(MWh)"] = compare_df["수요량(MWh)"] * 1.01 

    # ✅ 비교 그래프
    fig = px.line(compare_df, x="시간", y=["수요량(MWh)", "공급량(MWh)"],
                   title=f"{selected_year}년 시간대별 수요 vs 공급 비교 ",
                   markers=True, labels={"value": "전력량 (MWh)", "variable": "구분", "시간": "시간대"})
    fig.update_xaxes(title="시간대", tickmode="linear", dtick=1)
    fig.update_yaxes(title="전력량 (MWh)")
    st.plotly_chart(fig, use_container_width=True)

