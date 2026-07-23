import streamlit as st
import pandas as pd
import time
import random
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(
page_title="📚 Study Mate",
page_icon="📚",
layout="wide"
)

st.title("📚 Study Mate")
st.write("MBTI 기반 공부 메이트")

# =========================
# MBTI 데이터
# =========================

mbti_data = {
"INTJ": {
    "place": "스터디카페",
    "time": "22:00 ~ 01:00",
    "style": "계획표 작성 후 공부"
},
"ENFP": {
    "place": "카페",
    "time": "19:00 ~ 22:00",
    "style": "음악과 함께 공부"
},
"ISTP": {
    "place": "집",
    "time": "21:00 ~ 24:00",
    "style": "짧고 집중적으로 공부"
},
"INFJ": {
    "place": "도서관",
    "time": "20:00 ~ 23:00",
    "style": "조용한 환경에서 공부"
}
}

# =========================
# MBTI 선택
# =========================

st.header("🧠 MBTI 공부 추천")

mbti = st.selectbox(
"MBTI를 선택하세요.",
list(mbti_data.keys())
)

st.success(
f"""
추천 장소 : {mbti_data[mbti]['place']}

추천 시간 : {mbti_data[mbti]['time']}

추천 공부법 : {mbti_data[mbti]['style']}
"""
)

# =========================
# 공부 목표
# =========================

st.header("🎯 오늘의 목표")

goal = st.text_input(
"오늘의 공부 목표를 입력하세요."
)

if goal:
st.info(f"오늘의 목표 : {goal}")

# =========================
# 뽀모도로 타이머
# =========================

st.header("⏰ 뽀모도로 타이머")

if st.button("25분 공부 시작"):

progress = st.progress(0)

for i in range(100):
    time.sleep(0.1)
    progress.progress(i + 1)

st.success("25분 공부 완료! 5분 휴식하세요!")

# =========================
# 시간표 만들기
# =========================

st.header("📅 나의 시간표")

days = ["월", "화", "수", "목", "금"]
periods = [1, 2, 3, 4, 5, 6, 7]

schedule = {}

for day in days:

schedule[day] = []

for p in periods:

    subject = st.text_input(
        f"{day} {p}교시",
        key=f"{day}{p}"
    )

    schedule[day].append(subject)

df = pd.DataFrame(schedule)
df.index = [f"{i}교시" for i in periods]

st.dataframe(df)

# =========================
# 공부 레벨
# =========================

st.header("⭐ 공부 레벨")

hours = st.slider(
"이번 주 공부 시간",
0,
100,
10
)

if hours < 10:
level = "Lv.1 새싹"
elif hours < 30:
level = "Lv.2 공부러"
elif hours < 50:
level = "Lv.3 공부벌레"
else:
level = "Lv.4 학습 마스터"

st.success(f"현재 레벨 : {level}")

# =========================
# 오늘의 명언
# =========================

quotes = [
"작은 진전도 진전이다.",
"포기하지 않으면 실패가 아니다.",
"오늘의 노력이 내일의 결과를 만든다.",
"천천히 가도 멈추지만 않으면 된다."
]


st.header("💡 오늘의 명언")

st.info(random.choice(quotes))
# =========================
# 공부 시간 누적 저장
# =========================

if "total_minutes" not in st.session_state:
st.session_state.total_minutes = 0

if st.button("25분 공부 완료 기록"):
st.session_state.total_minutes += 25

total_hours = st.session_state.total_minutes / 60

st.write(
f"📚 총 공부 시간 : {total_hours:.1f}시간 "
f"({st.session_state.total_minutes}분)"
)
# =========================
# 출석 체크
# =========================

if "attendance" not in st.session_state:
st.session_state.attendance = 0

if st.button("오늘 공부 완료!"):
st.session_state.attendance += 1

st.success(
f"🔥 연속 공부 일수 : "
f"{st.session_state.attendance}일"
)

# =========================
# 시험 D-Day
# =========================

st.header("📅 시험 D-Day")

exam_date = st.date_input(
"시험 날짜를 선택하세요."
)

today = date.today()

days_left = (exam_date - today).days

if days_left > 0:
st.info(f"시험까지 D-{days_left}")
elif days_left == 0:
st.success("오늘이 시험날입니다!")
else:
st.warning("시험이 지났습니다.")
# =========================
# 공부 통계
# =========================

st.header("📈 공부 통계")

study_data = {
"월": 2,
"화": 1,
"수": 3,
"목": 4,
"금": 2,
"토": 5,
"일": 3
}

fig, ax = plt.subplots()

ax.bar(
study_data.keys(),
study_data.values()
)

ax.set_ylabel("공부 시간")

st.pyplot(fig)
if total_hours < 10:
level = "Lv.1 새싹 🌱"

elif total_hours < 30:
level = "Lv.2 공부러 📖"

elif total_hours < 50:
level = "Lv.3 공부벌레 🐛"

elif total_hours < 100:
level = "Lv.4 학습 마스터 🏆"

else:
level = "Lv.5 전설의 수험생 👑"

st.success(f"현재 레벨 : {level}")
