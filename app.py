import streamlit as st
import pandas as pd
import time
import os
import re
import asyncio
import edge_tts

# --- 1. 页面配置 & 马卡龙背景 ---
st.set_page_config(page_title="Chloe's Reading Space", layout="wide")
st.markdown("""<style>.stApp { background-color: #FFF5F7; } .stSidebar { background-color: #F0F7FF; }</style>""", unsafe_allow_html=True)

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

# 异步生成语音函数
async def generate_speech(text, voice, speed, output_path):
    # speed 格式如 "+10%" 或 "-10%"
    communicate = edge_tts.Communicate(text, voice, rate=speed)
    await communicate.save(output_path)

if df is not None:
    # --- 3. 侧边栏 ---
    st.sidebar.title("🌈 Chloe's Space")
    selected_title = st.sidebar.selectbox("📖 选择章节 | Select Chapter", df['title'].tolist())
    row = df[df['title'] == selected_title].iloc[0]

    safe_name = re.sub(r'[\\/:*?"<>|]', '_', selected_title)
    local_cn = f"audio/{safe_name}_CN.mp3"
    local_en = f"audio/{safe_name}_EN.mp3"

    st.sidebar.markdown("---")
    with st.sidebar.expander("🛠️ 语音操作间 (精准调速版)", expanded=False):
        # 语速调节滑块：默认 +20% 让中文听起来更干脆
        cn_speed = st.slider("中文语速调节", -20, 50, 10, step=5, format="%d%%")
        en_speed = st.slider("英文语速调节", -20, 50, 0, step=5, format="%d%%")
        
        t_zh = str(row.get('content_zh', ''))
        t_en = str(row.get('content_en', ''))

        if st.button("🔊 生成中文音频 (快速版)"):
            with st.spinner("正在用高级引擎转换中文..."):
                speed_str = f"{'+' if cn_speed>=0 else ''}{cn_speed}%"
                asyncio.run(generate_speech(t_zh, "zh-CN-XiaoxiaoNeural", speed_str, local_cn))
                st.rerun()
        
        if st.button("📢 生成英文音频"):
            with st.spinner("正在转换英文..."):
                speed_str = f"{'+' if en_speed>=0 else ''}{en_speed}%"
                asyncio.run(generate_speech(t_en, "en-US-EmmaNeural", speed_str, local_en))
                st.rerun()

    # --- 4. 主界面 ---
    st.title(selected_title)
    st.write(row.get('content_zh', ''))
    st.write(f"**{row.get('content_en', '')}**")

    # --- 5. 播放器 ---
    st.write("---")
    cloud_url = str(row.get('audio_url', '')).strip()
    if "http" in cloud_url and not cloud_url.startswith('nan'):
        st.audio(cloud_url)
    elif os.path.exists(local_cn) or os.path.exists(local_en):
        st.write("🔊 **语音内容已就绪 | Audio Ready**")
        c1, c2 = st.columns(2)
        if os.path.exists(local_cn):
            with c1: st.write("🇨🇳 中文"); st.audio(local_cn)
        if os.path.exists(local_en):
            with c2: st.write("🇬🇧 英文"); st.audio(local_en)

    # --- 6. 问答环节 (正则版) ---
    st.divider()
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
                        if idx == int(corrects[i]): st.success("✨ 答对了！"); st.balloons()
                        else: st.error("❌ 再想想！")
        except: st.write("题目加载中...")