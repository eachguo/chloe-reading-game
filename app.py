# 导入必备库（仅保留核心依赖，无冗余）
import streamlit as st
from streamlit_drawable_canvas import st_canvas

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
    .stExpander, .stHeader, .stSuccess, .stButton > button {
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

# ---------------------- 页面基础配置（最简，无报错） ----------------------
st.set_page_config(
    page_title="Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut",
    page_icon="📚",
    layout="centered"
)

# 调用背景函数（仅添加安全样式，不影响核心功能）
set_macaron_warm_background()

# ---------------------- 核心功能：双语内容 + 互动配对（全部保留） ----------------------
st.title("📚 Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut")
story_topic_cn = "《安妮的绿山墙》"
story_topic_en = "Anne of Green Gables"
st.subheader(f"—— {story_topic_cn} 专属阅读版 | Exclusive Reading Edition of {story_topic_en}")
st.divider()

# 中英双语段落
st.header("✨ 趣味段落阅读 | Fun Paragraph Reading")
with st.expander("📖 点击展开「英文原文」 | Click to Expand [English Original]", expanded=True):
    english_paragraph = """Anne Shirley was not what the Cuthberts had expected. 
They had sent for a boy to help them with the farm work, but instead, a thin, red-haired girl with big eyes stood before them."""
    st.write(english_paragraph)

with st.expander("📝 点击展开「中文翻译」 | Click to Expand [Chinese Translation]", expanded=True):
    chinese_paragraph = """安妮·雪莉并不是卡斯伯特兄妹所期待的那样。
他们本来申请了一个男孩来帮忙打理农场的活计，可站在他们面前的，却是一个瘦小、红头发、有着一双大眼睛的女孩。"""
    st.write(chinese_paragraph)

st.divider()

# 小思考问题
st.header("🤔 小思考问题 | Little Thinking Questions")
questions = [
    "1. What did the Cuthberts want at first? （卡斯伯特兄妹一开始想要什么？）",
    "2. What color is Anne's hair? （安妮的头发是什么颜色的？）"
]
for q in questions:
    st.write(f"✅ {q}")

st.divider()

# 互动单词配对（无复杂配置，确保正常运行）
st.header("🎮 单词配对小游戏 | Word Matching Game")
st.success("💡 游戏规则：用鼠标画线配对，提交后查看对错")

col1, col2 = st.columns(2)
with col1:
    st.subheader("英文单词 | English Words")
    st.write("1. orphanage")
    st.write("2. farm")
with col2:
    st.subheader("中文释义 | Chinese Meanings")
    st.write("A. 农场")
    st.write("B. 孤儿院")

st.write("### 🎨 点击下方画布画线配对")
canvas_result = st_canvas(
    fill_color="rgba(255,255,255,0)",
    stroke_width=3,
    stroke_color="#d48b6b",
    background_color="#fdf6f0",
    height=200,
    width=600,
    drawing_mode="freedraw",
    key="canvas"
)

if st.button("✅ 提交答案并判断 | Submit Answer and Judge"):
    st.write("### ✅ 正确配对：orphanage —— 孤儿院")
    st.write("### ❌ 错误示例：orphanage —— 农场")

st.divider()
st.write("### 🌟 下次我们一起阅读更多有趣的故事吧！ | Let's read more interesting stories next time!")