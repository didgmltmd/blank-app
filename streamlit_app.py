import streamlit as st
from dashboard.power_demand_dashboard import power_demand_dashboard
from dashboard.power_supply_dashboard import power_supply_dashboard
from dashboard.power_supply_vs_demand_dashboard import power_supply_vs_demand_dashboard
from dashboard.power_supply_vs_demand_outage_dashboard import power_outage_vs_supply_demand_dashboard

st.set_page_config(page_title="전력 통합 대시보드", layout="wide")

# 4개의 탭으로 구성
tab1, tab2, tab3, tab4 = st.tabs([
    "⚡ 전력수요 대시보드",
    "⚡ 전력공급 대시보드",
    "⚡ 전력 수요-공급 비교 대시보드",
    "⚡ 정전통계 + 수요·공급 비교"
])

with tab1:
    power_demand_dashboard()

with tab2:
    power_supply_dashboard()

with tab3:
    power_supply_vs_demand_dashboard()

with tab4:
    power_outage_vs_supply_demand_dashboard()
