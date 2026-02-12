import streamlit as st
import pandas as pd
import time
import os
import re
from gtts import gTTS 

# --- 1. 页面配置 & 马卡龙背景 ---
st.set_page_config(page_title="Chloe's Reading Space", layout="wide")
st.markdown("""<style>.stApp { background-color: #FFF5F7; } .stSidebar { background-color: #F0F7FF; }</style>""", unsafe_allow_html=True)

# 确保服务器环境有 audio 目录
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
    # --- 3. 侧边栏 & 制作人暗锁 ---
    st.sidebar.title("🌈 Chloe's Space")
    chapter_list = df['title'].tolist()
    selected_title = st.sidebar.selectbox("📖 选择章节 | Select Chapter", chapter_list)
    row = df[df['title'] == selected_title].iloc[0]

    # 清洗文件名用于匹配本地音频
    safe_name = re.sub(r'[\\/:*?"<>|]', '_', selected_title)
    local_cn = f"audio/{safe_name}_CN.mp3"
    local_en = f"audio/{safe_name}_EN.mp3"

    st.sidebar.markdown("---")
    with st.sidebar.expander("🛠️ 语音操作间 (制作人专用)", expanded=False):
        st.markdown("### 🎙️ AI 语音工场")
        t_zh = str(row.get('content_zh', ''))
        t_en = str(row.get('content_en', ''))
           if st.button("🔊 生成中文音频"):
            with st.spinner("中文转换中..."):
                # 将 slow=True 加入参数中，语速会明显变慢，适合跟读
                gTTS(text=t_zh, lang='zh-cn', slow=True).save(local_cn)
                st.success(f"已生成慢速中文音频！")
                st.rerun() 

    # --- 4. 主界面 (大宝阅读区) ---
    st.title(selected_title)
    st.write(row.get('content_zh', '内容准备中...'))
    st.write(f"**{row.get('content_en', 'Loading...')}**")

    # --- 5. 双语播放器 (正式版) ---
    st.write("---")
    # 逻辑：优先查找表格链接，其次查找本地生成的音频
    cloud_url = str(row.get('audio_url', '')).strip()
    
    if "http" in cloud_url and not cloud_url.startswith('nan'):
        st.write("🔊 **听听故事吧 | Listen to the Story**")
        st.audio(cloud_url)
    elif os.path.exists(local_cn) or os.path.exists(local_en):
        st.write("🔊 **语音内容已就绪 | Audio Content Ready**")
        col_cn, col_en = st.columns(2)
        if os.path.exists(local_cn):
            with col_cn:
                st.write("🇨🇳 **中文 | Chinese**")
                st.audio(local_cn)
        if os.path.exists(local_en):
            with col_en:
                st.write("🇬🇧 **英文 | English**")
                st.audio(local_en)
    else:
        st.info("✨ 朗读正在制作中... | Audio is being prepared!")

    # --- 6. 互动问答 (正则版) ---
    st.divider()
    st.subheader("🧠 互动问答 | Quiz Time")
    qz = str(row.get('quiz_json', ''))
    if qz and "[" in qz:
        try:
            questions = re.findall(r'\"question\":\s*\"(.*?)\"', qz)
            options_raw = re.findall(r'\"options\":\s*\[(.*?)\]', qz)
            corrects = re.findall(r'\"correct\":\s*(\d+)', qz)
            for i in range(len(questions)):
                st.write(f"**Q{i+1}: {questions[i]}**")
                opts = [o.strip().strip('"').strip("'") for o in options_raw[i].split(',')]
                cols = st.columns(len(opts))
                for idx, opt in enumerate(opts):
                    if cols[idx].button(opt, key=f"q_{safe_name}_{i}_{idx}"):
                        if idx == int(corrects[i]): st.success("✨ 答对了！ Well done!"); st.balloons()
                        else: st.error("❌ 再想想！ Try again!")
        except: st.warning("⚠️ 题目加载中...")