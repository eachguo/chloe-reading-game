import streamlit as st
import asyncio, edge_tts, os, re, sqlite3
from gtts import gTTS
from books_data import BOOKS 

# ---------------------- 1. 数据库初始化 ----------------------
def init_db():
    conn = sqlite3.connect('chloe_library.db')
    c = conn.cursor()
    # 创建书库表：编号, 标题, 英文内容, 中文内容, 英文音频, 中文音频
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id TEXT PRIMARY KEY, title TEXT, 
                  content_en TEXT, content_zh TEXT,
                  audio_en TEXT, audio_zh TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ---------------------- 2. 界面与导航 ----------------------
st.set_page_config(page_title="Chloe's Reading Space", page_icon="⚡")
is_admin = st.sidebar.checkbox("姥爷工作模式 | Grandpa Mode")
menu = ["📖 读书屋"] if not is_admin else ["📖 读书屋", "🎙️ 语音间", "⚙️ 后台维护"]
page = st.sidebar.radio("导航", menu)

# ---------------------- 3. 页面：读书屋 ----------------------
if "读书屋" in page:
    st.title("🧙‍♂️ Chloe's Reading Room")
    
    # 获取所有书籍（合并代码里的和数据库里的）
    conn = sqlite3.connect('chloe_library.db')
    c = conn.cursor()
    db_books = c.execute("SELECT * FROM books").fetchall()
    conn.close()
    
    # 建立一个统一的显示字典
    display_books = BOOKS.copy()
    for b in db_books:
        display_books[b[0]] = {
            "title": b[1], "content_en": b[2], "content_zh": b[3],
            "audio_en": b[4], "audio_zh": b[5], "quiz": []
        }
    
    book_key = st.selectbox("挑选你的故事：", list(display_books.keys()), 
                            format_func=lambda x: display_books[x]["title"])
    book = display_books[book_key]
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("English")
        st.write(book["content_en"])
        if os.path.exists(book["audio_en"]): st.audio(book["audio_en"])
    with col2:
        st.subheader("中文")
        st.write(book["content_zh"])
        if os.path.exists(book["audio_zh"]): st.audio(book["audio_zh"])

# ---------------------- 4. 页面：语音间 (双引擎版) ----------------------
elif page == "🎙️ 语音间":
    st.title("🎙️ 语音间 (双引擎备份)")
    txt = st.text_area("输入文字:")
    f_name = st.text_input("文件名 (不加后缀):", value="new_story")
    
    if st.button("🚀 生成音频"):
        if not os.path.exists("Audio"): os.makedirs("Audio")
        target = f"Audio/{f_name.strip()}.mp3"
        # 这里使用咱们之前成功的 gTTS 逻辑
        with st.spinner("施法中..."):
            try:
                lang = 'en' if 'en' in f_name else 'zh'
                tts = gTTS(text=txt, lang=lang)
                tts.save(target)
                st.success(f"✅ 生成成功！保存在 {target}")
                st.audio(target)
            except Exception as e:
                st.error(f"失败了: {e}")

# ---------------------- 5. 页面：后台维护 (数据库版) ----------------------
elif page == "⚙️ 后台维护":
    st.title("⚙️ 魔法书库录入中心")
    st.info("在这里录入的内容会直接存入数据库，不需要修改代码文件。")
    with st.form("add_db_book"):
        bid = st.text_input("书籍编号 (如: hp2)")
        title = st.text_input("书名 (双语)")
        en_txt = st.text_area("英文内容")
        zh_txt = st.text_area("中文内容")
        if st.form_submit_button("🚀 存入魔法仓库"):
            conn = sqlite3.connect('chloe_library.db')
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO books VALUES (?, ?, ?, ?, ?, ?)",
                      (bid, title, en_txt, zh_txt, f"Audio/{bid}_en.mp3", f"Audio/{bid}_zh.mp3"))
            conn.commit()
            conn.close()
            st.success(f"✅ 《{title}》已存入仓库！")