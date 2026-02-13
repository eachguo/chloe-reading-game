import streamlit as st
import pandas as pd
import asyncio
import edge_tts
import os
import json
import random

# --- 1. 界面与马卡龙主题 ---
st.set_page_config(page_title="Chloe's Magic Space", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFF5F5; }
    .main-box {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    .quiz-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #E0F2F1;
        margin-bottom: 20px;
        text-align: center;
    }
    h1 { color: #FF9AA2; font-family: 'Comic Sans MS', sans-serif; text-align: center; }
    /* 选项按钮样式：让它看起来像马卡龙颜色的卡片 */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        border: 2px solid #B2e2f2;
        background-color: #F0FBFF;
        color: #444;
        font-size: 18px;
        padding: 12px;
        margin-bottom: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FFD1DC; /* 鼠标悬停变粉色 */
        border-color: #FFB7B2;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# Google Sheets CSV 导出地址
SHEET_URL = "https://docs.google.com/spreadsheets/d/1BXjixKvVt5k1r9S7lqAzSJ_pxujAUZiODUd33KWxMNY/export?format=csv"

@st.cache_data(ttl=5)
def get_data(url):
    return pd.read_csv(url)

if st.sidebar.button("🔄 同步魔法书架"):
    st.cache_data.clear()
    st.rerun()

try:
    df = get_data(SHEET_URL)
except Exception as e:
    st.error(f"连接失败: {e}")
    st.stop()

# --- 2. 章节选择 ---
st.sidebar.title("📚 魔法书架")
chapter_options = df['title'].tolist()
selected_title = st.sidebar.selectbox("去哪一章？", chapter_options)
row = df[df['title'] == selected_title].iloc[0]
current_id = str(row.get('id', 'temp')).strip().lower()

# --- 3. 语音逻辑 ---
audio_folder = "Audio" if os.path.exists("Audio") else "audio"
path_zh = f"{audio_folder}/{current_id}_zh.mp3"
path_en = f"{audio_folder}/{current_id}_en.mp3"

# --- 4. 主界面内容 ---
st.title(f"🪄 {row['title']}")

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.subheader("🇨🇳 中文故事")
    st.write(row['content_zh'])
    if os.path.exists(path_zh): st.audio(path_zh)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.subheader("🇨🇦 English Story")
    st.write(row['content_en'])
    if os.path.exists(path_en): st.audio(path_en)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. 互动式问答 (即时反馈版) ---
st.markdown("---")
st.subheader("🧠 魔法小测试 | Quiz Time!")

# 有趣的反馈语库
success_messages = ["✨ 哇！Chloe 是不是偷偷用了魔法？全对！", "🎉 太棒了！你是霍格沃茨的一流学生！", "🌈 击掌！(High Five!) 你读得非常仔细！"]
wrong_messages = ["🤔 哎呀，分院帽说这个答案不太对哦，再试试？", "🕯️ 这里的灯光有点暗，再回故事里找找线索？", "🐾 差点就猜对了！再给魔法一个机会？"]

quiz_raw = row.get('quiz_json', '')
if pd.notna(quiz_raw) and str(quiz_raw).strip() != "":
    try:
        clean_json = str(quiz_raw).replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
        quiz_data = json.loads(clean_json)
        
        for i, q in enumerate(quiz_data):
            st.markdown(f'<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown(f"#### ❓ Question {i+1}")
            st.write(f"**{q['question']}**")
            
            correct_idx = int(q['correct'])
            for idx, option in enumerate(q['options']):
                if st.button(option, key=f"opt_{current_id}_{i}_{idx}"):
                    if idx == correct_idx:
                        st.success(random.choice(success_messages))
                        st.balloons()
                    else:
                        st.error(random.choice(wrong_messages))
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception:
        st.warning("⚠️ 问答加载出错，快去检查一下表格吧。")
else:
    st.info("这一章还没有准备好谜题。")