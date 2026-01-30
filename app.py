# 导入必备库（新增语音相关库，保留核心依赖）
import streamlit as st
from gtts import gTTS
from io import BytesIO, StringIO

# ---------------------- 马卡龙纯色背景（极简兼容，无图片，绝对不空白） ----------------------
def set_macaron_warm_background():
    """纯马卡龙浅蜜桃色背景，柔和不刺眼，兼容所有Streamlit版本"""
    background_css = """
    <style>
    /* 核心：纯马卡龙暖色系底色，无任何外部资源 */
    .stApp {
        background-color: #fff3e6 !important;
    }
    /* 文本区域加固，保证字迹清晰，不影响阅读 */
    .stExpander, .stHeader, .stSuccess, .stButton > button, .stTextInput > div > div, .stToggle > div {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 8px !important;
        padding: 10px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    /* 标题/分割线统一马卡龙暖橘色，视觉协调 */
    h1, h2, h3, h4 {
        color: #d48b6b !important;
    }
    .stDivider {
        border-top: 2px solid #d48b6b !important;
    }
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)

# ---------------------- 语音朗读功能（新增：中英文双语+开关控制） ----------------------
def text_to_speech(text, lang):
    """
    文本转语音函数
    :param text: 要转换的文本内容
    :param lang: 语言类型（'en' 英文，'zh-CN' 中文）
    :return: 语音字节流
    """
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        st.warning(f"⚠️ 语音生成失败：{str(e)} | Speech generation failed: {str(e)}")
        return None

# ---------------------- 页面基础配置（最简，无报错） ----------------------
st.set_page_config(
    page_title="Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut",
    page_icon="📚",
    layout="centered"
)

# 调用背景函数（仅添加安全样式，不影响核心功能）
set_macaron_warm_background()

# ---------------------- 核心功能：完整双语内容 + 语音朗读 + 优化版单词配对 ----------------------
st.title("Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut")
story_topic_cn = "《安妮的绿山墙》"
story_topic_en = "Anne of Green Gables"
st.subheader(f"—— {story_topic_cn} 专属阅读版 | Exclusive Reading Edition of {story_topic_en}")
st.divider()

# 新增：语音朗读开关（全局控制，中英文通用）
audio_toggle = st.toggle("开启/关闭语音朗读 | Enable/Disable Text-to-Speech", value=False)
st.caption("提示：开启后，展开阅读内容即可播放语音 | Tip: After enabling, expand the reading content to play audio.")
st.divider()

# 中英双语段落（完整内容 + 语音朗读功能）
st.header("趣味段落阅读 | Fun Paragraph Reading")

# 英文原文 + 语音朗读
with st.expander("点击展开「英文原文」 | Click to Expand [English Original]", expanded=True):
    english_paragraph = """Anne Shirley was not what the Cuthberts had expected. They had sent for a boy to help them with the farm work, but instead, a thin, red-haired girl with big eyes stood before them. She talked and talked, telling them about her life in the orphanage and her dreams of having a real home. Anne loved to imagine things—she called the cherry tree outside her window a "snow queen" and the brook a "silver thread". For her, the world was full of magic and beauty, even when life was hard. She hoped that the Cuthberts would keep her and that she would finally have a place to call home."""
    st.write(english_paragraph)
    
    # 语音播放：仅当开关开启时显示并生成语音
    if audio_toggle:
        st.subheader("英文语音朗读 | English Audio Reading")
        english_audio = text_to_speech(english_paragraph, lang='en')
        if english_audio:
            st.audio(english_audio, format='audio/mp3', label="English Passage Audio")

# 中文翻译 + 语音朗读
with st.expander("点击展开「中文翻译」 | Click to Expand [Chinese Translation]", expanded=True):
    chinese_paragraph = """安妮·雪莉并不是卡斯伯特兄妹所期待的那样。他们本来申请了一个男孩来帮忙打理农场的活计，可站在他们面前的，却是一个瘦小、红头发、有着一双大眼睛的女孩。她滔滔不绝地说着，跟他们讲述自己在孤儿院的生活，以及拥有一个真正家的梦想。安妮喜欢幻想——她把窗外的樱桃树称作“白雪女王”，把小溪称作“银线”。对她来说，即便生活艰难，这个世界也依然充满了魔法与美好。她希望卡斯伯特兄妹能留下她，希望自己终于能有一个可以称之为“家”的地方。"""
    st.write(chinese_paragraph)
    
    # 语音播放：仅当开关开启时显示并生成语音
    if audio_toggle:
        st.subheader("中文语音朗读 | Chinese Audio Reading")
        chinese_audio = text_to_speech(chinese_paragraph, lang='zh-CN')
        if chinese_audio:
            st.audio(chinese_audio, format='audio/mp3', label="Chinese Passage Audio")

st.divider()

# 小思考问题（完整列表，保持双语风格）
st.header("小思考问题 | Little Thinking Questions")
questions = [
    "1. What did the Cuthberts want at first? （卡斯伯特兄妹一开始想要什么？）",
    "2. What color is Anne's hair? （安妮的头发是什么颜色的？）",
    "3. What did Anne call the cherry tree? （安妮把樱桃树称作什么？）",
    "4. What was Anne's dream? （安妮的梦想是什么？）"
]
for q in questions:
    st.write(f"✅ {q}")

st.divider()

# ---------------------- 单词配对小游戏（最终优化版：隐藏答案提示 + 双语评判） ----------------------
st.header("单词配对小游戏 | Word Matching Game")
st.success("游戏规则：根据阅读内容，将英文单词与对应的中文释义配对，输入答案提交即可 | Game Rules: According to the passage, match English words with Chinese meanings, enter your answer and submit.")

# 第一步：展示单词列表（左右对齐，无泄露答案）
st.write("### 单词对应列表 | Word Matching List")
col1, col2 = st.columns(2)
with col1:
    st.subheader("英文单词 | English Words")
    st.write("1. orphanage")
    st.write("2. farm")
    st.write("3. dream")
    st.write("4. cherry tree")
with col2:
    st.subheader("中文释义 | Chinese Meanings")
    st.write("A. 农场")
    st.write("B. 孤儿院")
    st.write("C. 樱桃树")
    st.write("D. 梦想")

# 第二步：手动输入答案（隐藏直白答案，仅保留格式提示）
user_answer = st.text_input(
    label="请输入你的配对答案（格式提示：1X,2X,3X,4X，X为对应字母） | Enter your answer (Format: 1X,2X,3X,4X, X is the corresponding letter)",
    placeholder="例如：1A,2B,3C,4D | e.g.: 1A,2B,3C,4D",
    help="请严格按照格式输入，不要添加额外空格 | Please enter strictly according to the format, no extra spaces."
)

# 第三步：提交答案 + 双语评判反馈（无直白答案泄露，有悬念）
if st.button("提交答案并查看结果 | Submit Answer and Check Results"):
    # 预设正确答案（仅内部判断，不对外展示）
    correct_answer = "1B,2A,3D,4C"
    
    # 清理用户输入和正确答案（去除空格，转为大写，避免格式小误差导致误判）
    user_answer_clean = user_answer.replace(" ", "").upper()
    correct_answer_clean = correct_answer.replace(" ", "").upper()
    
    # 双语、有悬念的反馈逻辑
    if user_answer == "":
        st.warning("⚠️ 请先在输入框中输入你的答案哦！ | Please enter your answer in the input box first!")
    elif user_answer_clean == correct_answer_clean:
        st.success("🎉 太棒了！全部答对了，你太优秀了！ | Congratulations! You got all the answers right! You're amazing!")
    else:
        st.error("❌ 答案有误，请再仔细阅读文章，重新思考一下吧！ | Incorrect answers. Please read the passage again and think it over!")

st.divider()

# 底部结束语（双语风格）
st.write("### 下次我们一起阅读更多有趣的故事吧！ | Let's read more interesting stories next time!")