import streamlit as st
import asyncio, os, sqlite3, json
from gtts import gTTS
from books_data import BOOKS 

# ---------------------- 1. 数据库初始化 (自动补格子版) ----------------------
def init_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'chloe_library.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # 建立基础表
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id TEXT PRIMARY KEY, title TEXT, 
                  content_en TEXT, content_zh TEXT,
                  audio_en TEXT, audio_zh TEXT)''')
    # 核心修复：尝试增加 quiz_json 字段，如果已存在则跳过
    try:
        c.execute("ALTER TABLE books ADD COLUMN quiz_json TEXT")
    except:
        pass
    conn.commit()
    conn.close()

init_db()

# ---------------------- 2. 界面双语导航 ----------------------
st.set_page_config(page_title="Chloe's Reading Space", page_icon="⚡")
is_admin = st.sidebar.checkbox("姥爷工作模式 | Grandpa Mode")

menu_opts = {
    "Room": "📖 读书屋 | Reading Room", 
    "Voice": "🎙️ 语音间 | Voice Maker", 
    "Admin": "⚙️ 后台维护 | Admin"
}

if not is_admin:
    menu = [menu_opts["Room"]]
else:
    menu = [menu_opts["Room"], menu_opts["Voice"], menu_opts["Admin"]]

page = st.sidebar.radio("导航 | Navigation", menu)

# ---------------------- 3. 页面：读书屋 (全功能双语版) ----------------------
if menu_opts["Room"] in page:
    st.title("🧙‍♂️ Chloe's Magic Space")
    
    conn = sqlite3.connect('chloe_library.db')
    c = conn.cursor()
    db_books = c.execute("SELECT * FROM books").fetchall()
    conn.close()
    
    # 整合旧代码和新数据库的内容
    display_books = BOOKS.copy()
    for b in db_books:
        # 这里的索引 6 对应新增的 quiz_json
        display_books[b[0]] = {
            "title": b[1], "content_en": b[2], "content_zh": b[3],
            "audio_en": b[4], "audio_zh": b[5],
            "quiz": json.loads(b[6]) if (len(b) > 6 and b[6]) else []
        }
    
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

    # 问答区恢复
    if book.get("quiz"):
        st.divider()
        st.subheader("💡 魔法小测试 | Magic Quiz")
        for i, q in enumerate(book["quiz"]):
            st.write(f"**{q['question']}**")
            ans = st.radio(f"请选择 | Select (Q{i+1}):", q["options"], key=f"q_{book_key}_{i}")
            if st.button(f"检查答案 | Check Answer (Q{i+1})"):
                if q["options"].index(ans) == q["correct"]:
                    st.success("✨ 太棒了！答对了！ | Perfect! Correct!")
                else:
                    st.error("🧙‍♂️ 再试一次吧！ | Try again!")

# ---------------------- 4. 页面：语音间 (双引擎版) ----------------------
elif menu_opts["Voice"] in page:
    st.title("🎙️ 语音间 | Voice Maker")
    txt = st.text_area("输入文字 | Input Text:")
    f_name = st.text_input("文件名 | File Name (e.g., hp2_en):")
    if st.button("🚀 生成音频 | Generate Audio"):
        if not os.path.exists("Audio"): os.makedirs("Audio")
        target = f"Audio/{f_name.strip()}.mp3"
        with st.spinner("施法中..."):
            try:
                lang = 'en' if 'en' in f_name else 'zh'
                tts = gTTS(text=txt, lang=lang)
                tts.save(target)
                st.success(f"✅ 生成成功！保存在 {target}")
                st.audio(target)
            except Exception as e:
                st.error(f"失败: {e}")

# ---------------------- 5. 页面：后台维护 (支持问答录入) ----------------------
elif menu_opts["Admin"] in page:
    st.title("⚙️ 后台维护 | Admin")
    with st.form("full_add_form"):
        bid = st.text_input("编号 | ID (e.g., hp2)")
        title = st.text_input("书名 | Title (Bilingual)")
        en_txt = st.text_area("英文内容 | English Text")
        zh_txt = st.text_area("中文内容 | Chinese Text")
        st.write("--- 问答部分 | Quiz Section ---")
        q1 = st.text_input("问题 | Question")
        opt1 = st.text_input("选项 (用逗号隔开) | Options (split by comma)")
        correct1 = st.number_input("正确项索引 (0或1) | Correct Index", 0, 1)
        
        if st.form_submit_button("🚀 存入魔法仓库 | Save to Library"):
            # 将问答转为 JSON 格式存入数据库
            quiz_data = [{"question": q1, "options": [o.strip() for o in opt1.split(',')], "correct": int(correct1)}]
            conn = sqlite3.connect('chloe_library.db')
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO books VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (bid, title, en_txt, zh_txt, f"Audio/{bid}_en.mp3", f"Audio/{bid}_zh.mp3", json.dumps(quiz_data)))
            conn.commit()
            conn.close()
            st.success("✅ 完整双语内容已入库！")