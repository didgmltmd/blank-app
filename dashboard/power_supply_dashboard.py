import os
import pandas as pd
import streamlit as st
import plotly.express as px

# 데이터 디렉토리
DATA_DIR = "./data/전력공급"

def power_supply_dashboard():
    st.title("⚡ 전력공급 대시보드")

    tab1, tab2 = st.tabs([
        "지역별 전력 공급량",
        "시간대별 발전량 변화"
    ])

    # 1️⃣ 지역별 전력 공급량 (막대그래프)
    with tab1:
        st.subheader("지역별 전력 공급량 ")
        file_path = os.path.join(DATA_DIR, "HOME_발전·판매_발전량_지역별.xlsx")
        df = pd.read_excel(file_path, header=0)

        # ✅ 연도 선택
        available_years = df["연도"].unique()
        selected_year = st.selectbox("연도 선택", available_years)

        # ✅ 선택된 연도의 지역별 데이터만 필터링
        year_df = df[df["연도"] == selected_year]

        # ✅ 데이터를 melt해서 막대그래프 그리기
        df_melted = year_df.melt(id_vars="연도", var_name="지역", value_name="전력량")

        fig = px.bar(df_melted, x="지역", y="전력량",
                      title=f"{selected_year}년 지역별 전력 공급량",
                      color="지역", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("연도별 시간대별 평균 전력공급량")

        # 📁 파일 경로
        file1_path = os.path.join(DATA_DIR, "공급능력.csv")  # 2023~2025
        file2_path = os.path.join(DATA_DIR, "한국전력거래소_시간별 발전량_20211231.csv")  # 2017~

        # 📊 첫번째 파일 (공급능력)
        try:
            df1 = pd.read_csv(file1_path, encoding="utf-8")
        except UnicodeDecodeError:
            df1 = pd.read_csv(file1_path, encoding="euc-kr")
        df1.columns = [col.strip() for col in df1.columns]

        # ✅ 날짜 컬럼
        if "날짜" in df1.columns:
            df1["날짜"] = pd.to_datetime(df1["날짜"], errors="coerce")
        else:
            st.error("❌ 첫번째 파일에 '날짜' 컬럼이 없습니다!")

        df1["연도"] = df1["날짜"].dt.year

        # 📊 두번째 파일 (시간별 발전량)
        try:
            df2 = pd.read_csv(file2_path, encoding="utf-8")
        except UnicodeDecodeError:
            df2 = pd.read_csv(file2_path, encoding="euc-kr")
        df2.columns = [col.strip() for col in df2.columns]

        # ✅ 두번째 파일의 '거래일' 컬럼을 '날짜'로 통일
        if "거래일" in df2.columns:
            df2.rename(columns={"거래일": "날짜"}, inplace=True)
            df2["날짜"] = pd.to_datetime(df2["날짜"], errors="coerce")
        else:
            st.error("❌ 두번째 파일에 '거래일' 컬럼이 없습니다!")

        df2["연도"] = df2["날짜"].dt.year

        # ⏰ 시간대 컬럼 찾기
        hour_cols = [col for col in df1.columns if col.endswith("시")]

        # 🔗 두 데이터 합치기
        combined_df = pd.concat([df1[["연도"] + hour_cols], df2[["연도"] + hour_cols]], ignore_index=True)

        # 📅 연도 선택
        available_years = combined_df["연도"].dropna().unique()
        selected_year = st.selectbox("연도 선택", sorted(available_years))

        # 🔍 선택된 연도의 시간대별 평균 계산
        df_year = combined_df[combined_df["연도"] == selected_year]
        df_hourly_avg = df_year[hour_cols].mean().reset_index()
        df_hourly_avg.columns = ["시간", "발전량"]

        # ⏰ 시간대 정리
        df_hourly_avg["시간"] = df_hourly_avg["시간"].str.replace("시", "").astype(int)
        df_hourly_avg = df_hourly_avg.sort_values("시간")

        # 📈 그래프 그리기
        fig = px.line(df_hourly_avg, x="시간", y="발전량",
                    title=f"{selected_year}년 시간대별 평균 발전량",
                    markers=True, labels={"시간": "시간", "발전량": "발전량(MWh)"})
        fig.update_xaxes(title="시간", tickmode="linear", dtick=1)
        fig.update_yaxes(title="발전량 (MWh)")
        st.plotly_chart(fig, use_container_width=True)
