import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울시 공영주차장 안내",
    page_icon="🅿️",
    layout="wide"
)

st.title("🅿️ 서울시 공영주차장 안내 서비스")

# ----------------------------
# CSV 업로드
# ----------------------------

uploaded_file = st.file_uploader(
    "공영주차장 CSV 업로드",
    type=["csv"]
)

if uploaded_file is None:
    st.info("CSV 파일을 업로드해주세요.")
    st.stop()

# ----------------------------
# 데이터 읽기
# ----------------------------

try:
    df = pd.read_csv(uploaded_file, encoding="cp949")
except:
    df = pd.read_csv(uploaded_file, encoding="euc-kr")

# ----------------------------
# 데이터 전처리
# ----------------------------

df["기본 주차 요금"] = pd.to_numeric(
    df["기본 주차 요금"],
    errors="coerce"
)

df["일 최대 요금"] = pd.to_numeric(
    df["일 최대 요금"],
    errors="coerce"
)

df["위도"] = pd.to_numeric(df["위도"], errors="coerce")
df["경도"] = pd.to_numeric(df["경도"], errors="coerce")

df = df.dropna(subset=["위도", "경도"])

# ----------------------------
# 자치구 추출
# ----------------------------

df["자치구"] = df["주소"].str.extract(r"([가-힣]+구)")

districts = sorted(df["자치구"].dropna().unique())

selected_gu = st.sidebar.selectbox(
    "자치구 선택",
    ["전체"] + districts
)

# ----------------------------
# 필터
# ----------------------------

free_only = st.sidebar.checkbox("무료 주차장만")
night_free = st.sidebar.checkbox("야간 무료 개방")
weekend_free = st.sidebar.checkbox("주말 무료")

filtered = df.copy()

if selected_gu != "전체":
    filtered = filtered[
        filtered["자치구"] == selected_gu
    ]

if free_only:
    filtered = filtered[
        filtered["유무료구분명"] == "무료"
    ]

if night_free:
    filtered = filtered[
        filtered["야간무료개방여부명"]
        .astype(str)
        .str.contains("개방", na=False)
    ]

if weekend_free:
    filtered = filtered[
        filtered["토요일 유,무료 구분명"] == "무료"
    ]

# ----------------------------
# 가장 저렴한 주차장
# ----------------------------

st.subheader("💰 가장 저렴한 주차장")

cheap_df = filtered.dropna(
    subset=["기본 주차 요금"]
)

if len(cheap_df) > 0:

    cheapest = cheap_df.loc[
        cheap_df["기본 주차 요금"].idxmin()
    ]

    st.success(
        f"""
        📍 {cheapest['주차장명']}

        주소 : {cheapest['주소']}

        기본요금 : {int(cheapest['기본 주차 요금'])}원
        """
    )

# ----------------------------
# 지도 생성
# ----------------------------

if len(filtered) > 0:

    center_lat = filtered["위도"].mean()
    center_lon = filtered["경도"].mean()

else:

    center_lat = 37.5665
    center_lon = 126.9780

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=12
)

for _, row in filtered.iterrows():

    popup_html = f"""
    <b>{row['주차장명']}</b><br>
    주소: {row['주소']}<br>
    기본요금: {row['기본 주차 요금']}원<br>
    일최대요금: {row['일 최대 요금']}원<br>
    유무료: {row['유무료구분명']}<br>
    야간개방: {row['야간무료개방여부명']}<br>
    토요일: {row['토요일 유,무료 구분명']}<br>
    공휴일: {row['공휴일 유,무료 구분명']}
    """

    if row["유무료구분명"] == "무료":
        color = "green"
    else:
        color = "blue"

    folium.Marker(
        location=[row["위도"], row["경도"]],
        tooltip=popup_html,
        popup=popup_html,
        icon=folium.Icon(color=color)
    ).add_to(m)

st.subheader("🗺️ 공영주차장 지도")

st_folium(
    m,
    width=1200,
    height=700
)

# ----------------------------
# TOP 10 저렴한 주차장
# ----------------------------

st.subheader("🏆 요금이 저렴한 주차장 TOP 10")

rank_df = filtered[
    ["주차장명", "주소", "기본 주차 요금"]
].copy()

rank_df = rank_df.sort_values(
    "기본 주차 요금"
)

st.dataframe(
    rank_df.head(10),
    use_container_width=True
)

# ----------------------------
# 검색
# ----------------------------

st.subheader("🔍 주소 검색")

keyword = st.text_input(
    "주소 또는 주차장명 입력"
)

if keyword:

    result = filtered[
        filtered["주소"].astype(str).str.contains(keyword)
        |
        filtered["주차장명"].astype(str).str.contains(keyword)
    ]

    st.write(f"{len(result)}개 검색됨")

    st.dataframe(
        result,
        use_container_width=True
    )

# ----------------------------
# 다운로드
# ----------------------------

csv = filtered.to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    "📥 결과 다운로드",
    csv,
    "parking_result.csv",
    "text/csv"
)
