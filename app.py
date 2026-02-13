import streamlit as st
import pandas as pd
import asyncio
import edge_tts
import os
import json
import random

# --- 1. 极致视觉优化：清理干扰，适配手机 ---
st.set_page_config(page_title="Chloe's Magic Space", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFF5F5; }
    /* 彻底铲除顶部白色条条、装饰线和页眉 */
    [data-testid="stHeader"], [data-testid="stDecoration"], hr {
        display: none !important;
    }
    /* 压缩间距，让内容更紧凑 */
    .element-container, .stMarkdown {
        margin-bottom: 0px !important;
    }
    /* 自定义章节标题：字号1.6rem(适中)，无符号，粉色系 */
    .custom-title {
        color: #FF9AA2;
        font-family: 'Comic Sans MS', sans-serif;
        font-size: 1.6rem;
        font-weight: bold;
        padding: 20px 0 10px 0;
        text-align: left;
    }
    /* 内容卡片样式 */
    .main-box {
        background-color: #FFFFFF;
        padding: 18px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        margin-bottom: 15px;
    }
    /* 问答卡片样式 */
    .quiz-card {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #E0F2F1;
        margin-top: 10px;
    }
    /* 选项按钮：点一下就反馈 */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        border: 2px solid #B2e2f2;
        background-color: #F0FBFF;
        color: #444;
        font-size: 16px;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 您的 Google Sheets CSV 导出链接
SHEET_URL = "https://docs.google.com/spreadsheets/d/1BXjixKvVt5k1r9S7lqAzSJ_pxujAUZiODUd33KWxMNY/export?format=csv"

@st.cache_data(ttl=2)
def get_data(url):
    return pd.read_csv(url)

# --- 2. 侧边栏：魔法书架与隐藏设置 ---
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

# 侧边栏设置区 (双语提示，藏得深)
with st.sidebar.expander("⚙️ 设置 | Settings (姥爷专用/Grandpa Only)", expanded=False):
    st.caption("幕后制作区 / Production only.")
    if st.button("🔄 同步表格 | Sync Data"):
        st.cache_data.clear()
        st.rerun()
    cn_speed = st.slider("中文语速", -50, 50, 15)
    en_speed = st.slider("英文语速", -50, 50, 0)
    audio_folder = "Audio" if os.path.exists("Audio") else "audio"
    path_zh, path_en = f"{audio_folder}/{current_id}_zh.mp3", f"{audio_folder}/{current_id}_en.mp3"
    if st.button("🛠️ 重新录制 | Record"):
        async def make_audio():
            await edge_tts.Communicate(row['content_zh'], "zh-CN-XiaoxiaoNeural", rate=f"{'+' if cn_speed>=0 else ''}{cn_speed}%").save(path_zh)
            await edge_tts.Communicate(row['content_en'], "en-US-EmmaNeural", rate=f"{'+' if en_speed>=0 else ''}{en_speed}%").save(path_en)
        with st.spinner('录制中...'):
            asyncio.run(make_audio())
            st.rerun()

# --- 3. 主界面内容 ---
st.markdown(f'<div class="custom-title">{row["title"]}</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="main-box"><b>🇨🇳 中文故事</b><br><br>'+str(row['content_zh'])+'</div>', unsafe_allow_html=True)
    if os.path.exists(path_zh): st.audio(path_zh)

with col2:
    st.markdown('<div class="main-box"><b>🇨🇦 English Story</b><br><br>'+str(row['content_en'])+'</div>', unsafe_allow_html=True)
    if os.path.exists(path_en): st.audio(path_en)

# --- 4. 互动式问答 (双语评语版) ---
st.write("") 
st.subheader("🧠 魔法小测试 | Quiz Time!")

success_messages = [
    "✨ 哇！Chloe 是不是偷偷用了魔法？全对！ | Wow! Chloe, did you use magic? All correct!",
    "🎉 太棒了！你是霍格沃茨的一流学生！ | Great job! You're a top student at Hogwarts!",
    "🌈 击掌！你读得非常仔细！ | High five! You read very carefully!"
]
wrong_messages = [
    "🤔 哎呀，分院帽说再试试？ | Oops, the Sorting Hat says try again?",
    "🕯️ 再回故事里找找线索？ | Look for clues in the story again?",
    "🐾 差点就猜对了！再给魔法一个机会？ | Almost had it! Give magic another chance?"
]

quiz_raw = row.get('quiz_json', '')
if pd.notna(quiz_raw) and str(quiz_raw).strip() != "":
    try:
        clean_json = str(quiz_raw).replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
        quiz_data = json.loads(clean_json)
        for i, q in enumerate(quiz_data):
            st.markdown(f'<div class="quiz-card">', unsafe_allow_html=True)
            st.write(f"**Q{i+1}: {q['question']}**")
            correct_idx = int(q['correct'])
            for idx, option in enumerate(q['options']):
                if st.button(option, key=f"opt_{current_id}_{i}_{idx}"):
                    if idx == correct_idx:
                        st.success(random.choice(success_messages))
                        st.balloons()
                    else:
                        st.error(random.choice(wrong_messages))
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception: st.warning("⚠️ Quiz Data Error.")