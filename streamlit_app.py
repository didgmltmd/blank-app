import folium
import pandas as pd

df = pd.read_csv("/content/jinju_cctv_20250513.csv", encoding='euc-kr')




m = folium.Map(location=[35.1799817, 128.1076213], zoom_start=13)


for 위도, 경도, 목적 in zip(df['위도'], df['경도'], df['목적']):
    folium.Marker(location=[위도, 경도],
                  popup=folium.Popup(목적, parse_html=True, max_width=100)).add_to(m)

