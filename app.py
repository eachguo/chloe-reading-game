import streamlit as st
import pandas as pd
import time
import os
import re
import json
from gtts import gTTS 

# --- 1. 页面配置 & 马卡龙背景 ---
st.set_page_config(page_title="Chloe's Reading Space", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFF5F7; }
    .stSidebar { background-color: #F0F7FF; }
    /* 让侧边栏的文字颜色略显专业，区分于阅读区 */
    .stSidebar h3 { color: #4A90E2; }
    </style>
    """, unsafe_allow_html=True)

# 确保音频存放目录
if not os.path.exists("audio"):
    os.makedirs("audio")

# --- 2. 核心数据读取 ---
sh_url = f"https://docs.google.com/spreadsheets/d/1BXjixKvVt5k1r9S7lqAzSJ_pxujAUZiODUd33KWxMNY/gviz/tq?tqx=out:csv&v={int(time.time())}"

@st.cache_data(ttl=1)
def get_data(url):
    try:
        data = pd.read_csv(url)
        data.columns = [c.strip() for c in data.columns]
        return data
    except Exception as e:
        st.error(f"❌ 读取表格失败: {e}")
        return None

df = get_data(sh_url)

if df is not None and 'title' in df.columns:
    # --- 3. 侧边栏 (语音操作间：已加锁) ---
    st.sidebar.title("🌈 Chloe's Space")
    chapter_list = df['title'].tolist()
    selected_title = st.sidebar.selectbox("📖 选择章节 | Select Chapter", chapter_list)
    row = df[df['title'] == selected_title].iloc[0]

    st.sidebar.markdown("---")
    
    # 增加一个简单的折叠开关，作为给您的“暗锁”
    with st.sidebar.expander("🎧 语音操作间 (制作人专用)", expanded=False):
        st.markdown("### 🎙️ AI 语音工场")
        text_zh = str(row.get('content_zh', ''))
        text_en = str(row.get('content_en', ''))

        if st.button("🔊 生成中文音频"):
            with st.spinner("转换中..."):
                tts_zh = gTTS(text=text_zh, lang='zh-cn')
                path_zh = f"audio/{selected_title}_CN.mp3"
                tts_zh.save(path_zh)
                st.audio(path_zh)
                st.success(f"已存至: {path_zh}")

        if st.button("📢 生成英文音频"):
            with st.spinner("转换中..."):
                tts_en = gTTS(text=text_en, lang='en')
                path_en = f"audio/{selected_title}_EN.mp3"
                tts_en.save(path_en)
                st.audio(path_en)
                st.success(f"已存至: {path_en}")
        
        st.info("💡 请将生成的 MP3 上传云端，并将链接更新至 Google Sheets 的 audio_url 列。")

    # --- 4. 主界面 (大宝阅读区) ---
    st.title(selected_title)

    # 故事内容
    st.subheader("📜 故事内容 | Story Content")
    if 'content_zh' in row.index and pd.notna(row['content_zh']):
        st.write(row['content_zh'])
    if 'content_en' in row.index and pd.notna(row['content_en']):
        st.write(f"**{row['content_en']}**")

    # 朗读播放器 (仅在表格里有 http 链接时显示)
    audio_val = str(row.get('audio_url', '')).strip()
    if "http" in audio_val and not audio_val.startswith('nan'):
        st.write("---")
        st.write("🔊 **听听故事吧 | Listen to the Story**")
        st.audio(audio_val)

    st.divider()

    # --- 5. 互动问答 (接回之前的正则解析逻辑) ---
    st.subheader("🧠 互动问答 | Quiz Time")
    quiz_raw = str(row.get('quiz_json', ''))
    
    if quiz_raw and quiz_raw.strip() != "nan" and "[" in quiz_raw:
        try:
            # 使用您之前验证成功的正则匹配逻辑
            questions = re.findall(r'\"question\":\s*\"(.*?)\"', quiz_raw)
            options_raw = re.findall(r'\"options\":\s*\[(.*?)\]', quiz_raw)
            corrects = re.findall(r'\"correct\":\s*(\d+)', quiz_raw)

            for i in range(len(questions)):
                st.write(f"**Q{i+1}: {questions[i]}**")
                # 清洗选项
                opts_str = options_raw[i]
                opts = [opt.strip().strip('"').strip("'") for opt in opts_str.split(',')]
                
                cols = st.columns(len(opts))
                for idx, opt in enumerate(opts):
                    if cols[idx].button(opt, key=f"q_{selected_title}_{i}_{idx}"):
                        if idx == int(corrects[i]):
                            st.success("✨ 太棒了！答对了！ | Well done!")
                            st.balloons()
                        else:
                            st.error("❌ 哎呀，再想一想哦！ | Try again!")
        except Exception as e:
            st.warning("⚠️ 题目加载中...")
    else:
        st.write("✨ 本章暂时没有题目。")

else:
    st.info("🏠 正在开启阅读小屋...")