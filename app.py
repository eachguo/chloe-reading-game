import streamlit as st
import asyncio
import edge_tts
import os
import numpy as np
from scipy.io import wavfile
from io import BytesIO
from books_data import BOOKS 

# ---------------------- 1. 样式设置 ----------------------
st.set_page_config(page_title="Chloe's Reading Space", page_icon="📚", layout="centered")

def set_style():
    st.markdown("""
    <style>
    .stApp { background-color: #fff3e6 !important; }
    h1, h2, h3 { color: #d48b6b !important; text-align: center; }
    .stButton > button { background-color: white; border-radius: 12px; min-height: 3em; width: 100%; border: 1px solid #d48b6b; color: #5D4037; font-size: 16px; }
    .stButton > button:hover { background-color: #fdf2e9; border-color: #e67e22; }
    </style>
    """, unsafe_allow_html=True)

set_style()

def play_feedback_sound(is_correct):
    freq = 880 if is_correct else 220
    t = np.linspace(0, 0.2, int(44100 * 0.2), endpoint=False)
    tone = (0.2 * np.sin(2 * np.pi * freq * t) * 32767).astype(np.int16)
    buf = BytesIO()
    wavfile.write(buf, 44100, tone)
    st.audio(buf, format='audio/wav', autoplay=True)

# ---------------------- 2. 导航菜单 ----------------------
st.sidebar.title("🌈 导航菜单 | Navigation")
page = st.sidebar.radio("请选择：| Select:", 
    ["📖 故事屋 | Stories", "🎙️ 语音间 | Voice Maker", "⚙️ 后台管理 | Admin"])

# ---------------------- 3. 页面：故事屋 ----------------------
if page == "📖 故事屋 | Stories":
    st.title("📚 Chloe 的双语阅读小屋")
    book_key = st.selectbox("请挑选一本书：| Pick a book:", list(BOOKS.keys()), format_func=lambda x: BOOKS[x]["title"])
    book = BOOKS[book_key]
    
    st.divider()
    st.header(book["title"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"### 📖 English\n{book['content_en']}")
        # --- 增加防护：只有文件存在时才尝试播放 ---
        if book['audio_en']:
            if os.path.exists(book['audio_en']) or book['audio_en'].startswith("http"):
                st.audio(book["audio_en"])
            else:
                st.warning("⚠️ 英文语音文件还在录制中... | Audio coming soon...")
                
    with col2:
        st.write(f"### 📖 中文\n{book['content_zh']}")
        if book['audio_zh']:
            if os.path.exists(book['audio_zh']) or book['audio_zh'].startswith("http"):
                st.audio(book["audio_zh"])
            else:
                st.warning("⚠️ 中文语音文件还在录制中... | 语音录制中...")
    
    st.divider()
    st.header("🧠 互动小问答 | Quiz Time")
    for q_idx, q in enumerate(book.get("quiz", [])):
        st.subheader(q["question"])
        cols = st.columns(len(q["options"]))
        for i, opt in enumerate(q["options"]):
            if cols[i].button(opt, key=f"q_{book_key}_{q_idx}_{i}"):
                if i == q["correct"]:
                    st.success("🎉 答对啦！ | Correct!")
                    play_feedback_sound(True)
                else:
                    st.error("❌ 再试一次！ | Try again!")
                    play_feedback_sound(False)

# ---------------------- 4. 页面：语音间 ----------------------
elif page == "🎙️ 语音间 | Voice Maker":
    st.title("🎙️ 语音制作间 | Voice Maker")
    text_to_read = st.text_area("输入文字：")
    v_role = st.selectbox("选择朗读声音：", ["en-US-GuyNeural (狼先生)", "zh-CN-YunxiNeural (男童)", "fr-FR-EloiseNeural (法)"])
    f_name = st.text_input("文件名 (不带后缀):", value="bad_guys_en")
    
    if st.button("✨ 生成语音"):
        if text_to_read:
            async def do_tts():
                if not os.path.exists("Audio"): os.makedirs("Audio")
                await edge_tts.Communicate(text_to_read, v_role.split(' ')[0]).save(f"Audio/{f_name}.mp3")
            asyncio.run(do_tts())
            st.success(f"已生成！保存至 Audio/{f_name}.mp3")
            st.audio(f"Audio/{f_name}.mp3")

# ---------------------- 5. 页面：后台管理 ----------------------
elif page == "⚙️ 后台管理 | Admin":
    st.title("⚙️ 书单维护中心")
    with st.form("add_book"):
        bid = st.text_input("唯一编号 (如: guys_02)")
        title = st.text_input("书名 (双语)")
        en_c = st.text_area("英文内容")
        zh_c = st.text_area("中文内容")
        st.write("---")
        q_text = st.text_input("问题 (双语)")
        q_opts = st.text_input("选项 (用逗号隔开，如: 选项A, 选项B)")
        q_correct = st.number_input("正确项索引 (0代表第一个)", min_value=0, step=1)
        
        if st.form_submit_button("🚀 写入书库"):
            opts_list = [o.strip() for o in q_opts.split(',')]
            new_data = f"\nBOOKS['{bid}'] = {{'title': '{title}', 'audio_en': 'Audio/{bid}_en.mp3', 'audio_zh': 'Audio/{bid}_zh.mp3', 'content_en': \"\"\"{en_c}\"\"\", 'content_zh': \"\"\"{zh_c}\"\"\", 'quiz': [{{'question': '{q_text}', 'options': {opts_list}, 'correct': {q_correct}}}]}}"
            with open("books_data.py", "a", encoding="utf-8") as f:
                f.write(new_data)
            st.success("写入成功！")