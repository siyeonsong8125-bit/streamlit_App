import streamlit as st
import random

st.set_page_config(
    page_title="오늘 뭐 먹지? 🍽️",
    page_icon="🍜",
    layout="centered"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>

.stApp{
    background: linear-gradient(to bottom,#FFF7F8,#FFFDF5);
}

.title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#ff6b81;
}

.sub{
    text-align:center;
    color:#666;
    font-size:18px;
}

.box{
    background:white;
    border-radius:20px;
    padding:20px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.1);
}

.food{
    font-size:30px;
    color:#ff7f50;
    font-weight:bold;
    text-align:center;
}

.cal{
    text-align:center;
    color:#888;
    font-size:22px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🍴 오늘 뭐 먹지?</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>날씨에 맞는 메뉴를 추천해드려요 💕</div>", unsafe_allow_html=True)

# -----------------------------
# 데이터
# -----------------------------
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

weather = st.selectbox(
    "🌈 오늘 날씨를 선택하세요!",
    list(menus.keys())
)

if st.button("🍀 메뉴 추천받기"):
    food = random.choice(menus[weather])

    st.markdown("<div class='box'>", unsafe_allow_html=True)

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
st.caption("💗 Made with Streamlit")
