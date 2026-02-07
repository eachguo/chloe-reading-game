import streamlit as st
import asyncio, edge_tts, os, re, sqlite3
from gtts import gTTS
from books_data import BOOKS 

# ---------------------- 1. 数据库初始化 (书柜生成) ----------------------
def init_db():
    # 强制在当前文件夹生成数据库文件
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'chloe_library.db')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # 建立表格：编号, 标题, 英文内容, 中文内容, 英文音频路径, 中文音频路径
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

# ---------------------- 3. 页面：读书屋 (从代码+数据库读内容) ----------------------
if page == "📖 读书屋":
    st.title("🧙‍♂️ Chloe's Reading Room")
    
    # 获取数据库里的书
    conn = sqlite3.connect('chloe_library.db')
    c = conn.cursor()
    db_books = c.execute("SELECT * FROM books").fetchall()
    conn.close()
    
    # 合并 books_data.py 和 数据库 的内容
    display_books = BOOKS.copy()
    for b in db_books:
        display_books[b[0]] = {
            "title": b[1], "content_en": b[2], "content_zh": b[3],
            "audio_en": b[4], "audio_zh": b[5]
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

# ---------------------- 4. 页面：语音间 (双引擎备份) ----------------------
elif page == "🎙️ 语音间":
    st.title("🎙️ 语音间 (双引擎版)")
    txt = st.text_area("输入文字:")
    f_name = st.text_input("文件名 (如: hp2_en):", value="new_story")
    
    if st.button("🚀 生成音频"):
        if not os.path.exists("Audio"): os.makedirs("Audio")
        target = f"Audio/{f_name.strip()}.mp3"
        
        with st.spinner("施法中..."):
            # 尝试 gTTS 生成 (因为昨晚它在您的电脑上表现最稳)
            try:
                lang = 'en' if 'en' in f_name else 'zh'
                tts = gTTS(text=txt, lang=lang)
                tts.save(target)
                st.success(f"✅ 生成成功！保存在 {target}")
                st.audio(target)
            except Exception as e:
                st.error(f"语音生成失败: {e}")

# ---------------------- 5. 页面：后台维护 (数据库录入) ----------------------
elif page == "⚙️ 后台维护":
    st.title("⚙️ 魔法书库录入中心")
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