import streamlit as st
import requests
import random

# ------------------------
# 기본 설정
# ------------------------
st.set_page_config(
    page_title="오늘 뭐 먹지? 🍽️",
    page_icon="🍜",
    layout="centered"
)

# ------------------------
# CSS (귀여운 디자인)
# ------------------------
st.markdown("""
<style>

.stApp{
    background: linear-gradient(to bottom,#FFF7F8,#FFFDF5);
}

.title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#ff69b4;
}

.sub{
    text-align:center;
    color:#666666;
    font-size:18px;
}

.result{
    background:white;
    border-radius:20px;
    padding:20px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.15);
}

.food{
    text-align:center;
    font-size:30px;
    color:#ff7f50;
    font-weight:bold;
}

.cal{
    text-align:center;
    font-size:22px;
    color:#666;
}

.weather{
    text-align:center;
    font-size:22px;
    color:#3399ff;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🍴 오늘 뭐 먹지?</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>서울 날씨에 맞는 메뉴를 추천해드려요 💕</div>", unsafe_allow_html=True)

# ------------------------
# 메뉴 데이터
# ------------------------
menus = {

    "☀️ 맑음":[
        {
            "name":"냉모밀",
            "cal":480,
            "img":"https://images.unsplash.com/photo-1617093727343-374698b1b08d"
        },
        {
            "name":"비빔국수",
            "cal":520,
            "img":"https://images.unsplash.com/photo-1555126634-323283e090fa"
        },
        {
            "name":"샐러드",
            "cal":300,
            "img":"https://images.unsplash.com/photo-1546069901-ba9599a7e63c"
        }
    ],

    "🌧️ 비":[
        {
            "name":"김치전",
            "cal":610,
            "img":"https://images.unsplash.com/photo-1504674900247-0877df9cc836"
        },
        {
            "name":"칼국수",
            "cal":560,
            "img":"https://images.unsplash.com/photo-1617093727343-374698b1b08d"
        },
        {
            "name":"부대찌개",
            "cal":710,
            "img":"https://images.unsplash.com/photo-1544025162-d76694265947"
        }
    ],

    "❄️ 눈":[
        {
            "name":"떡국",
            "cal":520,
            "img":"https://images.unsplash.com/photo-1604908177522-432f3f5f87de"
        },
        {
            "name":"곰탕",
            "cal":620,
            "img":"https://images.unsplash.com/photo-1547592180-85f173990554"
        },
        {
            "name":"우동",
            "cal":470,
            "img":"https://images.unsplash.com/photo-1612929633738-8fe44f7ec841"
        }
    ],

    "🌤️ 흐림":[
        {
            "name":"돈까스",
            "cal":850,
            "img":"https://images.unsplash.com/photo-1544025162-d76694265947"
        },
        {
            "name":"제육볶음",
            "cal":700,
            "img":"https://images.unsplash.com/photo-1504674900247-0877df9cc836"
        },
        {
            "name":"덮밥",
            "cal":680,
            "img":"https://images.unsplash.com/photo-1512058564366-18510be2db19"
        }
    ],

    "🔥 더움":[
        {
            "name":"냉면",
            "cal":450,
            "img":"https://images.unsplash.com/photo-1617093727343-374698b1b08d"
        },
        {
            "name":"빙수",
            "cal":520,
            "img":"https://images.unsplash.com/photo-1563805042-7684c019e1cb"
        },
        {
            "name":"초밥",
            "cal":430,
            "img":"https://images.unsplash.com/photo-1579871494447-9811cf80d66c"
        }
    ]
}

# ------------------------
# 서울 날씨 가져오기
# ------------------------
API_KEY = st.secrets["OPENWEATHER_API_KEY"]

url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric&lang=kr"

response = requests.get(url)

if response.status_code != 200:
    st.error("서울 날씨를 불러오지 못했습니다.")
    st.stop()

data = response.json()

temp = data["main"]["temp"]
weather_main = data["weather"][0]["main"]
weather_desc = data["weather"][0]["description"]

# ------------------------
# 날씨 분류
# ------------------------
if weather_main == "Rain":
    weather = "🌧️ 비"

elif weather_main == "Snow":
    weather = "❄️ 눈"

elif temp >= 28:
    weather = "🔥 더움"

elif weather_main in ["Clouds", "Mist", "Fog", "Haze"]:
    weather = "🌤️ 흐림"

else:
    weather = "☀️ 맑음"

st.markdown(
    f"<div class='weather'>📍 서울 현재 날씨 : {weather_desc} / {temp:.1f}℃</div>",
    unsafe_allow_html=True
)

st.write("")

# ------------------------
# 메뉴 추천
# ------------------------
if st.button("🍀 오늘의 메뉴 추천"):

    food = random.choice(menus[weather])

    st.markdown("<div class='result'>", unsafe_allow_html=True)

    st.image(food["img"], use_container_width=True)

    st.markdown(
        f"<div class='food'>{food['name']}</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='cal'>🔥 {food['cal']} kcal</div>",
        unsafe_allow_html=True
    )

    st.success("맛있게 드세요 😋")

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.caption("💗 서울 실시간 날씨 기반 메뉴 추천 서비스")
