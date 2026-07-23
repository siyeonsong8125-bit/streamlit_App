import streamlit as st
import requests
import folium
import random

from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation

#------------------------
#기본 구조
#------------------------
API_KEY = st.secrets["GOOGLE_API_KEY"]

st.set_page_config(
    page_title="혼밥 메이트",
    page_icon="🍚",
    layout="wide"
)

st.title("🍚 혼밥 메이트")
#--------------------------
#현재 위치 가져오기
#--------------------------
location = streamlit_geolocation()

if location:
    lat = location["latitude"]
    lng = location["longitude"]
  #---------------------------
  #Nearby Search
  #---------------------------
  url = (
    "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
)

params = {
    "location": f"{lat},{lng}",
    "radius": 1000,
    "type": "restaurant",
    "key": API_KEY
}

response = requests.get(url, params=params).json()

restaurants = response["results"]
#---------------------------------------
#혼밥 점수
#----------------------------------
def honbab_score(place):

    score = 50

    if place.get("rating", 0) >= 4.5:
        score += 15

    if place.get("user_ratings_total", 0) > 100:
        score += 10

    if place.get("price_level", 2) <= 2:
        score += 10

    if place.get("opening_hours", {}).get(
        "open_now",
        False
    ):
        score += 10

    return min(score, 100)
  # ==========================
# 사용자 혼밥 평가 시스템
# ==========================

st.subheader("📝 내가 평가하기")

taste = st.slider(
    "🍽️ 맛",
    min_value=1,
    max_value=5,
    value=3
)

mood = st.slider(
    "✨ 분위기",
    min_value=1,
    max_value=5,
    value=3
)

solo = st.slider(
    "🍚 혼밥 편의성",
    min_value=1,
    max_value=5,
    value=3
)

revisit = st.slider(
    "🔄 재방문 의사",
    min_value=1,
    max_value=5,
    value=3
)

# 사용자 점수 계산
# 혼밥 편의성에 가중치(40%) 부여

user_score = (
    taste * 0.2 +
    mood * 0.2 +
    solo * 0.4 +
    revisit * 0.2
) * 20

st.write(f"### 내 평가 점수 : {user_score:.1f}점")

# AI 혼밥 점수 예시
# (기존 honbab_score() 함수의 결과값 사용)
ai_score = score

# 최종 점수 계산
final_score = (ai_score * 0.7) + (user_score * 0.3)

st.success(
    f"""
    🤖 AI 혼밥 점수 : {ai_score:.1f}점

    🙋 내 점수 : {user_score:.1f}점

    🏆 최종 혼밥 점수 : {final_score:.1f}점
    """
)

# 평가 저장
if "reviews" not in st.session_state:
    st.session_state.reviews = {}

if st.button("평가 저장"):
    st.session_state.reviews[place["name"]] = {
        "맛": taste,
        "분위기": mood,
        "혼밥 편의성": solo,
        "재방문 의사": revisit,
        "사용자 점수": round(user_score, 1),
        "최종 점수": round(final_score, 1)
    }

    st.success(f"{place['name']} 평가가 저장되었습니다!")

# 저장된 평가 표시
if place["name"] in st.session_state.reviews:

    saved = st.session_state.reviews[place["name"]]

    st.info(
        f"""
        ### 📌 저장된 내 평가

        - 맛 : {saved['맛']}/5
        - 분위기 : {saved['분위기']}/5
        - 혼밥 편의성 : {saved['혼밥 편의성']}/5
        - 재방문 의사 : {saved['재방문 의사']}/5

        사용자 점수 : {saved['사용자 점수']}점
        최종 점수 : {saved['최종 점수']}점
        """
    )
  #------------------------
  #지도표시
  #------------------------
  m = folium.Map(
    location=[lat, lng],
    zoom_start=15
)

for place in restaurants:

    score = honbab_score(place)

    popup = f"""
    <h4>{place['name']}</h4>
    평점 : {place.get('rating','-')}<br>
    리뷰 수 : {place.get('user_ratings_total',0)}<br>
    혼밥 점수 : {score}
    """

    folium.Marker(
        [
            place["geometry"]["location"]["lat"],
            place["geometry"]["location"]["lng"]
        ],
        popup=popup
    ).add_to(m)

st_folium(
    m,
    width=1000,
    height=600
)
#-------------------------
#랜덤 추천
#--------------------------
if st.button("오늘의 혼밥 추천"):

    choice = random.choice(restaurants)

    st.success(
        f"""
        {choice['name']}

        평점 : {choice.get('rating')}

        혼밥 점수 :
        {honbab_score(choice)}
        """
    )
  #---------------------------
  #즐겨찾기
  #----------------------------
  if "favorites" not in st.session_state:
    st.session_state.favorites = []

for place in restaurants:

    if st.button(
        f"{place['name']} 저장"
    ):
        st.session_state.favorites.append(
            place["name"]
        )
#--------------------------------
#AI 리뷰 요약
#--------------------------------
def summarize(text):

    if "혼자" in text:
        return (
            "혼자 방문하기 좋은 분위기입니다."
        )

    return (
        "전반적으로 만족도가 높습니다."
    )
#----------------------------------
#사이드바
#----------------------------------
with st.sidebar:

    st.header("필터")

    menu = st.selectbox(
        "메뉴",
        [
            "전체",
            "한식",
            "중식",
            "일식",
            "양식"
        ]
    )

    level = st.slider(
        "혼밥 레벨",
        1,
        5,
        3
    )

    price = st.selectbox(
        "가격",
        [
            "전체",
            "1만원 이하",
            "1~2만원",
            "2만원 이상"
        ]
    )
