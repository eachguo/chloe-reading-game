import streamlit as st
import pandas as pd
import asyncio
import edge_tts
import os
import json

# --- 1. 界面与马卡龙主题 ---
st.set_page_config(page_title="Chloe's Magic Space", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFF5F5; }
    .main-box {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    h1 { color: #FF9AA2; font-family: 'Comic Sans MS'; }
    .stButton>button { background-color: #B2e2f2; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 强制转换 CSV 链接并加上随机数防止缓存
SHEET_URL = "https://docs.google.com/spreadsheets/d/1BXjixKvVt5k1r9S7lqAzSJ_pxujAUZiODUd33KWxMNY/export?format=csv"

# --- 2. 获取数据 (加了缓存清理按钮) ---
@st.cache_data(ttl=5) # 极短缓存
def get_data(url):
    return pd.read_csv(url)

if st.sidebar.button("🔄 刷新表格数据"):
    st.cache_data.clear()
    st.rerun()

try:
    df = get_data(SHEET_URL)
except Exception as e:
    st.error(f"连接魔法书架失败: {e}")
    st.stop()

# --- 3. 章节选择 ---
st.sidebar.title("📚 魔法书架")
chapter_options = df['title'].tolist()
selected_title = st.sidebar.selectbox("去哪一章？", chapter_options)
row = df[df['title'] == selected_title].iloc[0]

# 统一 ID 识别
current_id = str(row.get('id', 'temp')).strip().lower()

# --- 4. 语音实验室 (语速调节藏在里面) ---
with st.sidebar.expander("🛠️ 语音实验室 (姥爷专用)", expanded=False):
    cn_speed = st.slider("中文语速 (%)", -50, 50, 15, key="cn_sp")
    en_speed = st.slider("英文语速 (%)", -50, 50, 0, key="en_sp")
    
    # 自动识别文件夹名 (Audio 或 audio)
    audio_folder = "Audio" if os.path.exists("Audio") else "audio"
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)
        
    path_zh = f"{audio_folder}/{current_id}_zh.mp3"
    path_en = f"{audio_folder}/{current_id}_en.mp3"

    if st.button("🔊 重新生成当前页语音"):
        async def make_audio():
            await edge_tts.Communicate(row['content_zh'], "zh-CN-XiaoxiaoNeural", rate=f"{'+' if cn_speed>=0 else ''}{cn_speed}%").save(path_zh)
            await edge_tts.Communicate(row['content_en'], "en-US-EmmaNeural", rate=f"{'+' if en_speed>=0 else ''}{en_speed}%").save(path_en)
        asyncio.run(make_audio())
        st.success("✅ 语音已重制！")
        st.rerun()

# --- 5. 主界面内容 ---
st.title(f"📖 {row['title']}")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.subheader("🇨🇳 中文故事")
    st.write(row['content_zh'])
    if os.path.exists(path_zh):
        st.audio(path_zh)
    else:
        st.info(f"等待同步: {path_zh}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.subheader("🇨🇦 English Story")
    st.write(row['content_en'])
    if os.path.exists(path_en):
        st.audio(path_en)
    else:
        st.info(f"Waiting for audio: {path_en}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. 问答环节 (增强版) ---
st.markdown("---")
st.subheader("🧠 魔法小测试 | Quiz")

quiz_raw = row.get('quiz_json', '')
if pd.notna(quiz_raw) and str(quiz_raw).strip() != "":
    try:
        # 处理中文引号问题
        clean_json = str(quiz_raw).replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
        quiz_data = json.loads(clean_json)
        
        for i, q in enumerate(quiz_data):
            st.write(f"**Q{i+1}: {q['question']}**")
            user_choice = st.radio("选择答案:", q['options'], key=f"radio_{current_id}_{i}")
            if st.button(f"提交答案 {i+1}", key=f"btn_{current_id}_{i}"):
                if q['options'].index(user_choice) == int(q['correct']):
                    st.success("✨ 太棒了！答对了！")
                    st.balloons()
                else:
                    st.error("❌ 哎呀，再想想看？")
    except Exception as e:
        st.warning(f"问答格式有误，请检查表格 JSON 格式。")
else:
    st.info("这一章还没有准备好谜题哦。")