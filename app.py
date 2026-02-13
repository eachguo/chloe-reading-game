import streamlit as st
import pandas as pd
import asyncio
import edge_tts
import os
import json
import random

# --- 1. 界面优化：只精准删除杂质，保留系统功能 ---
st.set_page_config(page_title="Chloe's Magic Space", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFF5F5; }
    
    /* 1. 只删除页面顶部的黑色装饰条和多余空白，保留侧边栏按钮 */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        color: #FF9AA2 !important;
    }
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* 2. 自定义章节标题：字号1.6rem，无任何前缀符号 */
    .custom-title {
        color: #FF9AA2;
        font-family: 'Comic Sans MS', sans-serif;
        font-size: 1.6rem;
        font-weight: bold;
        padding: 5px 0 10px 0;
        margin-top: -20px;
    }
    
    .main-box {
        background-color: #FFFFFF;
        padding: 18px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        margin-bottom: 15px;
    }
    
    .quiz-card {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #E0F2F1;
        margin-top: 10px;
    }

    .stButton>button {
        width: 100%;
        border-radius: 12px;
        border: 2px solid #B2e2f2;
        background-color: #F0FBFF;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

# Google Sheets CSV 导出链接
SHEET_URL = "https://docs.google.com/spreadsheets/d/1BXjixKvVt5k1r9S7lqAzSJ_pxujAUZiODUd33KWxMNY/export?format=csv"

@st.cache_data(ttl=2)
def get_data(url):
    return pd.read_csv(url)

# --- 2. 侧边栏 ---
st.sidebar.title("📚 Chloe's Space")

try:
    df = get_data(SHEET_URL)
except Exception as e:
    st.error(f"连接失败: {e}")
    st.stop()

chapter_options = df['title'].tolist()
selected_title = st.sidebar.selectbox("选择章节 | Select Chapter", chapter_options)
row = df[df['title'] == selected_title].iloc[0]
current_id = str(row.get('id', 'temp')).strip().lower()

# 侧边栏设置 (双语)
with st.sidebar.expander("⚙️ Settings (姥爷专用)", expanded=False):
    if st.button("🔄 Sync Data"):
        st.cache_data.clear()
        st.rerun()
    cn_speed = st.slider("中文语速", -50, 50, 15)
    en_speed = st.slider("英文语速", -50, 50, 0)
    audio_folder = "Audio" if os.path.exists("Audio") else "audio"
    path_zh, path_en = f"{audio_folder}/{current_id}_zh.mp3", f"{audio_folder}/{current_id}_en.mp3"
    if st.button("🛠️ Record"):
        async def make_audio():
            await edge_tts.Communicate(row['content_zh'], "zh-CN-XiaoxiaoNeural", rate=f"{'+' if cn_speed>=0 else ''}{cn_speed}%").save(path_zh)
            await edge_tts.Communicate(row['content_en'], "en-US-EmmaNeural", rate=f"{'+' if en_speed>=0 else ''}{en_speed}%").save(path_en)
        asyncio.run(make_audio()); st.rerun()

# --- 3. 主界面内容 ---
# 这里的 custom-title 已经彻底去掉了任何符号
st.markdown(f'<div class="custom-title">{row["title"]}</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="main-box"><b>🇨🇳 中文故事</b><br><br>'+str(row['content_zh'])+'</div>', unsafe_allow_html=True)
    if os.path.exists(path_zh): st.audio(path_zh)

with col2:
    st.markdown('<div class="main-box"><b>🇨🇦 English Story</b><br><br>'+str(row['content_en'])+'</div>', unsafe_allow_html=True)
    if os.path.exists(path_en): st.audio(path_en)

# --- 4. 互动问答 ---
st.subheader("🧠 魔法小测试 | Quiz Time!")
success_messages = ["✨ 哇！全对！ | Wow! All correct!", "🎉 太棒了！ | Great job!", "🌈 击掌！ | High five!"]
wrong_messages = ["🤔 再试试？ | Try again?", "🕯️ 找找线索？ | Look for clues?", "🐾 差点就对了！ | Almost!"]

quiz_raw = row.get('quiz_json', '')
if pd.notna(quiz_raw) and str(quiz_raw).strip() != "":
    try:
        clean_json = str(quiz_raw).replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
        quiz_data = json.loads(clean_json)
        for i, q in enumerate(quiz_data):
            st.markdown(f'<div class="quiz-card">', unsafe_allow_html=True)
            st.write(f"**Q{i+1}: {q['question']}**")
            for idx, option in enumerate(q['options']):
                if st.button(option, key=f"opt_{current_id}_{i}_{idx}"):
                    if idx == int(q['correct']):
                        st.success(random.choice(success_messages)); st.balloons()
                    else:
                        st.error(random.choice(wrong_messages))
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception: st.warning("⚠️ Quiz Data Error.")