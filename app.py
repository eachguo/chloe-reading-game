# 导入必备库（只保留必须的，无额外依赖）
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# ---------------------- 页面基础配置（最简版） ----------------------
st.set_page_config(
    page_title="Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut",
    page_icon="📚",
    layout="centered"
)

# ---------------------- 页面主标题（双语，无额外样式） ----------------------
st.title("📚 Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut")
story_topic_cn = "《安妮的绿山墙》"
story_topic_en = "Anne of Green Gables"
st.subheader(f"—— {story_topic_cn} 专属阅读版 | Exclusive Reading Edition of {story_topic_en}")
st.divider()

# ---------------------- 第一部分：中英双语段落（最简排版） ----------------------
st.header("✨ 趣味段落阅读 | Fun Paragraph Reading")

# 英文原文
with st.expander("📖 点击展开「英文原文」 | Click to Expand [English Original]", expanded=True):
    english_paragraph = """Anne Shirley was not what the Cuthberts had expected. 
They had sent for a boy to help them with the farm work, but instead, a thin, red-haired girl with big eyes stood before them."""
    st.write(english_paragraph)

# 中文翻译
with st.expander("📝 点击展开「中文翻译」 | Click to Expand [Chinese Translation]", expanded=True):
    chinese_paragraph = """安妮·雪莉并不是卡斯伯特兄妹所期待的那样。
他们本来申请了一个男孩来帮忙打理农场的活计，可站在他们面前的，却是一个瘦小、红头发、有着一双大眼睛的女孩。"""
    st.write(chinese_paragraph)

st.divider()

# ---------------------- 第二部分：小思考问题 ----------------------
st.header("🤔 小思考问题 | Little Thinking Questions")
questions = [
    "1. What did the Cuthberts want at first? （卡斯伯特兄妹一开始想要什么？）",
    "2. What color is Anne's hair? （安妮的头发是什么颜色的？）"
]
for q in questions:
    st.write(f"✅ {q}")

st.divider()

# ---------------------- 第三部分：互动单词配对（最简版） ----------------------
st.header("🎮 单词配对小游戏 | Word Matching Game")
st.success("💡 游戏规则：用鼠标画线配对，提交后查看对错")

# 左右两列单词
col1, col2 = st.columns(2)
with col1:
    st.subheader("英文单词 | English Words")
    st.write("1. orphanage")
    st.write("2. farm")
with col2:
    st.subheader("中文释义 | Chinese Meanings")
    st.write("A. 农场")
    st.write("B. 孤儿院")

# 互动画布
st.write("### 🎨 点击下方画布画线配对")
canvas_result = st_canvas(
    fill_color="rgba(255,255,255,0)",
    stroke_width=3,
    stroke_color="#000000",
    background_color="#f5f5f5",
    height=200,
    width=600,
    drawing_mode="freedraw",
    key="canvas"
)

# 提交按钮
if st.button("✅ 提交答案并判断 | Submit Answer and Judge"):
    st.write("### ✅ 正确配对：orphanage —— 孤儿院")
    st.write("### ❌ 错误示例：orphanage —— 农场")

st.divider()

# ---------------------- 底部结束语 ----------------------
st.write("### 🌟 下次我们一起阅读更多有趣的故事吧！ | Let's read more interesting stories next time!")