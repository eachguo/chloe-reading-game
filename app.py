import streamlit as st
import pandas as pd
import os
import asyncio
import edge_tts
from books_data import BOOKS # 保留最初的5个内置故事

# ---------------------- 1. 主程序配置 ----------------------
st.set_page_config(page_title="Chloe's Reading Space", page_icon="⚡")

# ---------------------- 2. 魔法装修：背景与双语样式 ----------------------
def set_bg_style():
    st.markdown(
        """
        <style>
        .stApp { background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%); }
        .stSelectbox div[data-baseweb="select"] { border-radius: 15px; border: 2px solid #a1887f; }
        h1 { color: #5d4037; font-family: 'Comic Sans MS', cursive, sans-serif; text-shadow: 2px 2px 4px #ffffff; }
        .stButton>button { border-radius: 20px; background-color: #a1887f; color: white; border: none; }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------------- 3. 语音生成逻辑 (Edge-TTS) ----------------------
async def generate_voice(text, filename, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

# ---------------------- 4. 云端书库连接 (Google Sheets) ----------------------
SHEET_URL = "https://docs.google.com/spreadsheets/d/1BXjixKvVt5k1r9S7lqAzSJ_pxujAUZiODUd33KWxMNY/export?format=csv"

def load_data():
    # 融合本地 BOOKS 和云端 Google Sheets 内容
    display_books = BOOKS.copy()
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [c.strip().lower() for c in df.columns]
        for _, row in df.iterrows():
            display_books[str(row['id'])] = {
                "title": str(row['title']),
                "content_en": str(row['content_en']),
                "content_zh": str(row['content_zh']),
                "audio_en": str(row['audio_en']),
                "audio_zh": str(row['audio_zh']),
                "quiz": eval(str(row['quiz_json'])) if (pd.notna(row['quiz_json']) and str(row['quiz_json']).strip() != "") else []
            }
    except Exception as e:
        pass # 如果表格暂不可读，至少还有本地的基础故事
    return display_books

# ---------------------- 5. 程序运行逻辑 ----------------------
set_bg_style()
st.sidebar.title("Navigation | 导航")
is_admin = st.sidebar.checkbox("姥爷工作模式 | Grandpa Mode")

menu_opts = {
    "Room": "📖 读书屋 | Reading Room", 
    "Voice": "🎙️ 语音间 | Voice Maker"
}

menu = [menu_opts["Room"]] if not is_admin else [menu_opts["Room"], menu_opts["Voice"]]
page = st.sidebar.radio("Go to:", menu)

# --- 页面 1：读书屋 ---
if menu_opts["Room"] in page:
    st.title("🧙‍♂️ Chloe's Magic Space")
    display_books = load_data()
    
    book_key = st.selectbox("挑选你的故事 | Pick your story:", list(display_books.keys()), 
                            format_func=lambda x: display_books[x]["title"])
    book = display_books[book_key]
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("English 🇺🇸")
        st.write(book["content_en"])
        if os.path.exists(book["audio_en"]): st.audio(book["audio_en"])
    with col2:
        st.subheader("中文 🇨🇳")
        st.write(book["content_zh"])
        if os.path.exists(book["audio_zh"]): st.audio(book["audio_zh"])

    if book.get("quiz"):
        st.divider()
        st.subheader("💡 魔法小测试 | Magic Quiz")
        for i, q in enumerate(book["quiz"]):
            st.write(f"**{q['question']}**")
            ans = st.radio(f"请选择 | Select:", q["options"], key=f"q_{book_key}_{i}")
            if st.button(f"检查答案 | Check Answer", key=f"btn_{i}"):
                if q["options"].index(ans) == q["correct"]:
                    st.success("✨ 太棒了！答对了！ | Perfect! Correct!")
                else:
                    st.error("🧙‍♂️ 再试一次吧！ | Try again!")

# --- 页面 2：语音间 ---
elif menu_opts["Voice"] in page:
    st.title("🎙️ 语音工作室 | Voice Maker")
    text_input = st.text_area("输入文字 | Input Text:")
    col_a, col_b = st.columns(2)
    with col_a:
        lang_type = st.radio("选择语言 | Language:", ["English", "中文"])
        voice_option = "en-US-AnaNeural" if lang_type == "English" else "zh-CN-XiaoxiaoNeural"
    with col_b:
        file_id = st.text_input("书籍编号 (如 hp4):", value="hp4")
        final_name = f"Audio/{file_id}{'_en' if lang_type == 'English' else '_zh'}.mp3"

    if st.button("🚀 生成并试听 | Generate & Listen"):
        if text_input:
            if not os.path.exists("Audio"): os.makedirs("Audio")
            asyncio.run(generate_voice(text_input, final_name, voice_option))
            st.success(f"已存入本地 Audio 文件夹")
            st.audio(final_name)