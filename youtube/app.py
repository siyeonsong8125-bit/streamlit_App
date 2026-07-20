import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from googleapiclient.discovery import build
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Okt
from textblob import TextBlob
import re
import numpy as np

# =========================
# 페이지 설정
# =========================

st.set_page_config(
    page_title="유튜브 댓글 분석기",
    page_icon="📊",
    layout="wide"
)

st.title("📊 유튜브 댓글 분석기")
st.markdown("유튜브 링크를 입력하면 댓글을 분석합니다.")

# =========================
# API KEY
# =========================

API_KEY = st.secrets["YOUTUBE_API_KEY"]

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

# =========================
# 폰트 경로
# =========================

FONT_PATH = "NanumGothic.ttf"

# =========================
# 영상 ID 추출
# =========================

def get_video_id(url):
    patterns = [
        r"v=([^&]+)",
        r"youtu\.be/([^?]+)"
    ]

    for p in patterns:
        match = re.search(p, url)
        if match:
            return match.group(1)

    return None

# =========================
# 댓글 수집
# =========================

def get_comments(video_id, max_comments):

    comments = []
    times = []

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )

    while request and len(comments) < max_comments:

        response = request.execute()

        for item in response["items"]:

            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]

            published = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]

            comments.append(comment)
            times.append(published)

            if len(comments) >= max_comments:
                break

        request = youtube.commentThreads().list_next(
            request,
            response
        )

    return pd.DataFrame({
        "comment": comments,
        "time": times
    })

# =========================
# 감성 분석
# =========================

def sentiment(text):

    score = TextBlob(text).sentiment.polarity

    if score > 0.1:
        return "긍정"

    elif score < -0.1:
        return "부정"

    else:
        return "중립"

# =========================
# 워드클라우드
# =========================

def make_wordcloud(texts):

    okt = Okt()

    nouns = []

    for text in texts:
        nouns.extend(okt.nouns(text))

    nouns = [n for n in nouns if len(n) >= 2]

    text = " ".join(nouns)

    wc = WordCloud(
        font_path=FONT_PATH,
        background_color="white",
        width=1000,
        height=500
    )

    return wc.generate(text)

# =========================
# 입력
# =========================

url = st.text_input(
    "유튜브 링크 입력"
)

max_comments = st.slider(
    "분석할 댓글 수",
    100,
    1000,
    500,
    100
)

# =========================
# 분석 시작
# =========================

if st.button("분석 시작"):

    video_id = get_video_id(url)

    if not video_id:
        st.error("올바른 유튜브 링크를 입력하세요.")
        st.stop()

    # ---------------------
    # 영상 표시
    # ---------------------

    st.subheader("🎥 영상")

    st.video(url)

    # ---------------------
    # 댓글 수집
    # ---------------------

    with st.spinner("댓글 수집 중..."):

        df = get_comments(
            video_id,
            max_comments
        )

    st.success(f"{len(df)}개 댓글 수집 완료")

    # ---------------------
    # 댓글 시간 분석
    # ---------------------

    st.subheader("📈 시간대별 댓글 작성 추이")

    df["time"] = pd.to_datetime(df["time"])

    hourly = (
        df
        .groupby(df["time"].dt.hour)
        .size()
        .reset_index(name="count")
    )

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(
        hourly["time"],
        hourly["count"],
        marker="o"
    )

    ax.set_xlabel("시간")
    ax.set_ylabel("댓글 수")
    ax.set_title("시간대별 댓글 작성 추이")

    st.pyplot(fig)

    # ---------------------
    # 감성 분석
    # ---------------------

    st.subheader("😊 댓글 반응도 분석")

    df["sentiment"] = df["comment"].apply(sentiment)

    sentiment_count = df["sentiment"].value_counts()

    fig2, ax2 = plt.subplots()

    ax2.pie(
        sentiment_count,
        labels=sentiment_count.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig2)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "긍정",
        sentiment_count.get("긍정", 0)
    )

    col2.metric(
        "중립",
        sentiment_count.get("중립", 0)
    )

    col3.metric(
        "부정",
        sentiment_count.get("부정", 0)
    )

    # ---------------------
    # 워드클라우드
    # ---------------------

    st.subheader("☁️ 댓글 워드클라우드")

    wc = make_wordcloud(
        df["comment"]
    )

    fig3, ax3 = plt.subplots(
        figsize=(12,6)
    )

    ax3.imshow(wc)

    ax3.axis("off")

    st.pyplot(fig3)

    # ---------------------
    # 자주 등장한 단어
    # ---------------------

    st.subheader("🔍 자주 등장한 단어 TOP 20")

    okt = Okt()

    nouns = []

    for comment in df["comment"]:
        nouns.extend(okt.nouns(comment))

    nouns = [n for n in nouns if len(n) >= 2]

    top_words = Counter(nouns).most_common(20)

    word_df = pd.DataFrame(
        top_words,
        columns=["단어", "빈도"]
    )

    st.dataframe(
        word_df,
        use_container_width=True
    )
