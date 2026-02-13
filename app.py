import streamlit as st
import pandas as pd
import asyncio
import edge_tts
import os
import json
import random

# --- 1. 界面与马卡龙主题（针对手机端微调） ---
st.set_page_config(page_title="Chloe's Magic Space", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFF5F5; }
    /* 卡片容器：去掉多余边距 */
    .main-box {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    /* 2. 章节标题字号调小，去掉装饰符 */
    .custom-title {
        color: #FF9AA2;
        font-family: 'Comic Sans MS', sans-serif;
        font-size: 1.8rem; /* 调小字号 */
        font-weight: bold;
        margin-top: -30px; /* 压缩顶部空白 */
        margin-bottom: 20px;
    }
    .quiz-card {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #E0F2F1;
        margin-bottom: 15px;
    }
    /* 选项按钮：保持趣味性 */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        border: 2px solid #B2e2f2;
        background-color: #F0FBFF;
        color: #444;
        font-size: 16px;
        margin-bottom: 5px;
    }
    /* 移除特定条状装饰物 */
    [data-testid="stHorizontalBlock"] {
        gap: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Google Sheets CSV 链接
SHEET_URL = "https://docs.google.com/spreadsheets/d/1BXjixKvVt5k1r9S7lqAzSJ_pxujAUZiODUd33KWxMNY/export?format=csv"

@st.cache_data(ttl=2)
def get_data(url):
    return pd.read_csv(url)

# --- 2. 侧边栏导航 ---
st.sidebar.title("📚 Chloe's Magic Space")

try:
    df = get_data(SHEET_URL)
except Exception as e:
    st.error(f"连接失败: {e}")
    st.stop()

chapter_options = df['title'].tolist()
selected_title = st.sidebar.selectbox("选择章节 | Select Chapter", chapter_options)
row = df[df['title'] == selected_title].iloc[0]
current_id = str(row.get('id', 'temp')).strip().lower()

st.sidebar.markdown("---")

# --- 3. 语音设置 (增加双语提示，藏得更深) ---
with st.sidebar.expander("⚙️ 设置 | Settings (姥爷专用/Grandpa Only)", expanded=False):
    st.caption("这里是幕后制作区 / For production use only.")
    if st.button("🔄 同步表格 | Sync Data"):
        st.cache_data.clear()
        st.rerun()
    
    cn_speed = st.slider("中文语速", -50, 50, 15)
    en_speed = st.slider("英文语速", -50, 50, 0)
    
    audio_folder = "Audio" if os.path.exists("Audio") else "audio"
    path_zh = f"{audio_folder}/{current_id}_zh.mp3"
    path_en = f"{audio_folder}/{current_id}_en.mp3"

    if st.button("🛠️ 重新录制这一页 | Record This Page"):
        async def make_audio():
            await edge_tts.Communicate(row['content_zh'], "zh-CN-XiaoxiaoNeural", rate=f"{'+' if cn_speed>=0 else ''}{cn_speed}%").save(path_zh)
            await edge_tts.Communicate(row['content_en'], "en-US-EmmaNeural", rate=f"{'+' if en_speed>=0 else ''}{en_speed}%").save(path_en)
        with st.spinner('魔法录制中...'):
            asyncio.run(make_audio())
            st.rerun()

# --- 4. 主界面内容 ---
# 使用自定义样式替代 st.title，解决字号和符号问题
st.markdown(f'<div class="custom-title">{row["title"]}</div>', unsafe_allow_html=True)

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

# --- 5. 互动式问答 ---
st.markdown("---")
st.subheader("🧠 魔法小测试 | Quiz Time!")

success_messages = ["✨ 哇！Chloe 是不是偷偷用了魔法？全对！", "🎉 太棒了！你是霍格沃茨的一流学生！", "🌈 High Five! You read it carefully!"]
wrong_messages = ["🤔 哎呀，分院帽说这个答案不太对哦，再试试？", "🕯️ 再回故事里找找线索？", "🐾 Almost there! Try again!"]

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
    except Exception:
        st.warning("⚠️ 问答加载出错。")