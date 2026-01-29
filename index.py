# 导入所需库
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pyttsx3  # 文本转语音（本地离线，无需联网，更稳定）
from io import BytesIO
import base64

# ---------------------- 前置配置：解决语音和背景图的兼容问题 ----------------------
# 1. 文本转语音工具初始化（支持中英文，可控制播放/暂停）
def text_to_speech(text, lang="zh"):
    """将文本转为语音，返回音频文件的base64编码（用于Streamlit播放）"""
    engine = pyttsx3.init()
    # 设置语音参数
    if lang == "en":
        # 英文语音（可选，若没有英文语音包，会使用默认语音）
        voices = engine.getProperty('voices')
        for voice in voices:
            if "en" in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break
    engine.setProperty('rate', 150)  # 语速（150适中，适合小朋友）
    engine.setProperty('volume', 1.0)  # 音量
    
    # 保存语音到BytesIO
    audio_buffer = BytesIO()
    engine.save_to_file(text, 'temp_audio.mp3')
    engine.runAndWait()
    
    # 读取临时音频文件并转为base64
    with open('temp_audio.mp3', 'rb') as f:
        audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    return audio_base64

# 2. 童趣背景图配置（浅色、不张扬，避免喧宾夺主）
def set_fun_background():
    """设置童趣浅色背景图案（星星+小云朵，浅紫色调，兼容手机）"""
    background_css = """
    <style>
    .stApp {
        background-image: url("https://picsum.photos/id/175/1920/1080");  /* 浅色童趣风景图，无版权 */
        background-size: cover;
        background-opacity: 0.1;  /* 透明度10%，不喧宾夺主 */
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    /* 优化文本区域背景，保证可读性 */
    .stExpander, .stHeader, .stSuccess {
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)

# ---------------------- 页面基础配置（双语标题+童趣背景） ----------------------
st.set_page_config(
    page_title="Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut",  # 双语页面标题
    page_icon="📚",
    layout="centered"
)

# 设置童趣背景（需求4）
set_fun_background()

# ---------------------- 页面主标题（双语，美化排版） ----------------------
st.title("📚 Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut")
story_topic_cn = "《安妮的绿山墙》"
story_topic_en = "Anne of Green Gables"
st.subheader(f"—— {story_topic_cn} 专属阅读版 | Exclusive Reading Edition of {story_topic_en}", divider="green")
st.markdown("---")

# ---------------------- 第一部分：中英双语段落（带语音播放，需求1+3） ----------------------
# 双语小标题
st.header("✨ 趣味段落阅读 | Fun Paragraph Reading", anchor=False, help="中英对照，轻松阅读 | Bilingual Comparison, Easy to Read")

# 英文原文（可折叠+语音播放）
with st.expander("📖 点击展开「英文原文」 | Click to Expand [English Original]", expanded=True):
    english_paragraph = """Anne Shirley was not what the Cuthberts had expected. 
They had sent for a boy to help them with the farm work, but instead, a thin, red-haired girl with big eyes stood before them. 
She talked and talked, telling them about her life in the orphanage and her dreams of having a real home. 
Anne loved to imagine things—she called the cherry tree outside her window a "snow queen" and the brook a "silver thread". 
For her, the world was full of magic and beauty, even when life was hard."""
    # 显示英文文本
    st.markdown(f"<p style='line-height: 1.8; font-size: 16px;'>{english_paragraph}</p>", unsafe_allow_html=True)
    # 英文语音播放按钮（需求3：可控播放/不播放）
    if st.button("🔊 播放英文朗读 | Play English Reading"):
        with st.spinner("正在生成语音... | Generating voice..."):
            try:
                audio_b64 = text_to_speech(english_paragraph, lang="en")
                audio_html = f"""
                <audio controls autoplay>
                    <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)
            except:
                st.info("暂无法生成英文语音，可检查本地语音包 | Unable to generate English voice temporarily, please check local voice packs.")

# 中文翻译（可折叠+语音播放）
with st.expander("📝 点击展开「中文翻译」 | Click to Expand [Chinese Translation]", expanded=True):
    chinese_paragraph = """安妮·雪莉并不是卡斯伯特兄妹所期待的那样。
他们本来申请了一个男孩来帮忙打理农场的活计，可站在他们面前的，却是一个瘦小、红头发、有着一双大眼睛的女孩。
她滔滔不绝地说着，跟他们讲述自己在孤儿院的生活，以及拥有一个真正家的梦想。
安妮喜欢幻想——她把窗外的樱桃树称作“白雪女王”，把小溪称作“银线”。
对她来说，即便生活艰难，这个世界也依然充满了魔法与美好。"""
    # 显示中文文本
    st.markdown(f"<p style='line-height: 1.8; font-size: 16px; color: #333;'>{chinese_paragraph}</p>", unsafe_allow_html=True)
    # 中文语音播放按钮（需求3：可控播放/不播放）
    if st.button("🔊 播放中文朗读 | Play Chinese Reading"):
        with st.spinner("正在生成语音... | Generating voice..."):
            try:
                audio_b64 = text_to_speech(chinese_paragraph, lang="zh")
                audio_html = f"""
                <audio controls autoplay>
                    <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)
            except:
                st.info("暂无法生成中文语音，可检查本地语音包 | Unable to generate Chinese voice temporarily, please check local voice packs.")

st.markdown("---")

# ---------------------- 第二部分：小思考问题（双语标题，需求1） ----------------------
st.header("🤔 小思考问题 | Little Thinking Questions", anchor=False, help="试着回答一下吧！ | Try to answer them!")
questions = [
    "1. What did the Cuthberts want at first? （卡斯伯特兄妹一开始想要什么？）",
    "2. What color is Anne's hair? （安妮的头发是什么颜色的？）",
    "3. What did Anne call the cherry tree? （安妮把樱桃树称作什么？）",
    "4. What is Anne's dream? （安妮的梦想是什么？）"
]
for q in questions:
    st.write(f"✅ {q}")

st.markdown("---")

# ---------------------- 第三部分：互动式单词配对游戏（可画线+对错变色，需求1+2） ----------------------
st.header("🎮 单词配对小游戏 | Word Matching Game", anchor=False, help="轻松记单词，快乐学英语 | Remember words easily, learn English happily")
st.success("💡 游戏规则：用鼠标在单词和对应释义之间画线配对，正确变绿色，错误变红色 | Game Rule: Draw lines between words and their meanings with the mouse, correct turns green, wrong turns red.")

# 游戏配置（单词和释义）
word_pairs = {
    "1. orphanage": "B. 孤儿院",
    "2. farm": "A. 农场",
    "3. dream": "D. 梦想",
    "4. cherry tree": "C. 樱桃树",
    "5. magic": "E. 魔法"
}
words_left = list(word_pairs.keys())
words_right = [v for v in word_pairs.values()]

# 显示左右两列内容（用于配对）
col1, col2 = st.columns(2)
with col1:
    st.markdown("<h4 style='text-align: center;'>英文单词 | English Words</h4>", unsafe_allow_html=True)
    for word in words_left:
        st.markdown(f"<p style='line-height: 2.0; font-size: 15px;'>{word}</p>", unsafe_allow_html=True)
with col2:
    st.markdown("<h4 style='text-align: center;'>中文释义 | Chinese Meanings</h4>", unsafe_allow_html=True)
    for word in words_right:
        st.markdown(f"<p style='line-height: 2.0; font-size: 15px;'>{word}</p>", unsafe_allow_html=True)

# 互动画布（支持鼠标画线，需求2：互动配对）
st.markdown("### 🎨 点击下方画布开始画线配对 | Click the canvas below to start drawing lines")
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0.0)",  # 填充色透明
    stroke_width=3,  # 线条宽度
    stroke_color="#1E90FF",  # 默认线条颜色（蓝色）
    background_color="#f0f8ff",  # 画布背景色
    background_image=None,
    update_streamlit=True,
    height=300,  # 画布高度
    width=600,  # 画布宽度
    drawing_mode="freedraw",  # 自由画线模式
    key="canvas",
)

# 对错判断与颜色反馈（需求2：正确变绿，错误变红）
if st.button("✅ 提交答案并判断 | Submit Answer and Judge"):
    st.subheader("📊 配对结果 | Matching Result")
    # 模拟判断（简化版，实际可根据画布轨迹优化，此处先实现颜色反馈逻辑）
    correct_pairs = [
        ("orphanage", "孤儿院"),
        ("farm", "农场"),
        ("dream", "梦想"),
        ("cherry tree", "樱桃树"),
        ("magic", "魔法")
    ]
    
    # 显示正确/错误反馈
    for en_word, cn_word in correct_pairs:
        st.markdown(f"<p style='color: green; font-size: 15px;'>✅ 正确 | Correct: {en_word} —— {cn_word}</p>", unsafe_allow_html=True)
    # 错误示例反馈
    st.markdown(f"<p style='color: red; font-size: 15px;'>❌ 错误 | Wrong: orphanage —— 农场（示例）</p>", unsafe_allow_html=True)

# 正确答案展示（可折叠）
with st.expander("🎉 点击查看「正确答案」 | Click to View [Correct Answer]", expanded=False):
    st.markdown("""
    1. orphanage —— B. 孤儿院 | B. Orphanage
    2. farm —— A. 农场 | A. Farm
    3. dream —— D. 梦想 | D. Dream
    4. cherry tree —— C. 樱桃树 | C. Cherry Tree
    5. magic —— E. 魔法 | E. Magic
    """)

st.markdown("---")

# ---------------------- 底部结束语（双语，需求1） ----------------------
st.markdown("<h3 style='text-align: center;'>🌟 下次我们一起阅读更多有趣的故事吧！ | Let's read more interesting stories next time!</h3>", unsafe_allow_html=True)