import streamlit as st
import pandas as pd
import time
import os
import re
from gtts import gTTS 

# --- 1. 页面配置 & 马卡龙背景 ---
st.set_page_config(page_title="Chloe's Reading Space", layout="wide")
st.markdown("""<style>.stApp { background-color: #FFF5F7; } .stSidebar { background-color: #F0F7FF; }</style>""", unsafe_allow_html=True)

# 确保服务器上有 audio 目录
if not os.path.exists("audio"):
    os.makedirs("audio")

# --- 2. 数据读取 ---
sh_url = f"https://docs.google.com/spreadsheets/d/1BXjixKvVt5k1r9S7lqAzSJ_pxujAUZiODUd33KWxMNY/gviz/tq?tqx=out:csv&v={int(time.time())}"
@st.cache_data(ttl=1)
def get_data(url):
    try:
        df = pd.read_csv(url)
        df.columns = [c.strip() for c in df.columns]
        return df
    except: return None

df = get_data(sh_url)

if df is not None:
    # --- 3. 侧边栏 (先定义章节变量) ---
    st.sidebar.title("🌈 Chloe's Space")
    chapter_list = df['title'].tolist()
    selected_title = st.sidebar.selectbox("📖 选择章节", chapter_list)
    row = df[df['title'] == selected_title].iloc[0]

    # --- 4. 路径定义 (解决 NameError) ---
    local_cn = f"audio/{selected_title}_CN.mp3"
    local_en = f"audio/{selected_title}_EN.mp3"

    with st.sidebar.expander("🎧 语音操作间 (制作人专用)", expanded=False):
        text_zh = str(row.get('content_zh', ''))
        text_en = str(row.get('content_en', ''))
        if st.button("🔊 生成中文音频"):
            gTTS(text=text_zh, lang='zh-cn').save(local_cn)
            st.rerun() # 生成后强制刷新，让播放器出现
        if st.button("📢 生成英文音频"):
            gTTS(text=text_en, lang='en').save(local_en)
            st.rerun()

    # --- 5. 主界面 (大宝阅读区) ---
    st.title(selected_title)
    st.write(row.get('content_zh', ''))
    st.write(f"**{row.get('content_en', '')}**")

    # --- 自动播放器逻辑 ---
    st.write("---")
    audio_link = str(row.get('audio_url', '')).strip()
    
    if "http" in audio_link and not audio_link.startswith('nan'):
        st.write("🔊 **听听故事吧 | Listen**")
        st.audio(audio_link)
    elif os.path.exists(local_cn) or os.path.exists(local_en):
        st.write("🔊 **临时试听区 (待上传) | Preview**")
        c1, c2 = st.columns(2)
        if os.path.exists(local_cn): c1.audio(local_cn)
        if os.path.exists(local_en): c2.audio(local_en)
    else:
        st.info("✨ 朗读制作中... | Coming soon!")

    # --- 6. 问答环节 (正则版) ---
    st.divider()
    quiz_raw = str(row.get('quiz_json', ''))
    if quiz_raw and "[" in quiz_raw:
        try:
            questions = re.findall(r'\"question\":\s*\"(.*?)\"', quiz_raw)
            options_raw = re.findall(r'\"options\":\s*\[(.*?)\]', quiz_raw)
            corrects = re.findall(r'\"correct\":\s*(\d+)', quiz_raw)
            for i in range(len(questions)):
                st.write(f"**Q{i+1}: {questions[i]}**")
                opts = [opt.strip().strip('"').strip("'") for opt in options_raw[i].split(',')]
                cols = st.columns(len(opts))
                for idx, opt in enumerate(opts):
                    if cols[idx].button(opt, key=f"q_{selected_title}_{i}_{idx}"):
                        if idx == int(corrects[i]): st.success("✨ 答对了！"); st.balloons()
                        else: st.error("❌ 再想想！")
        except: st.warning("⚠️ 题目排版中...")