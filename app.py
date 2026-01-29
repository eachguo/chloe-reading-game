import streamlit as st
from streamlit_drawable_canvas import st_canvas

# 页面基础配置
st.set_page_config(
    page_title="Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut",
    page_icon="📚",
    layout="centered"
)

# 页面主标题
st.title("📚 Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut")
st.subheader("—— 《安妮的绿山墙》专属阅读版 | Exclusive Reading Edition of Anne of Green Gables", divider="green")
st.markdown("---")

# 第一部分：中英双语段落
st.header("✨ 趣味段落阅读 | Fun Paragraph Reading")
with st.expander("📖 点击展开「英文原文」 | Click to Expand [English Original]", expanded=True):
    english_paragraph = """Anne Shirley was not what the Cuthberts had expected. 
They had sent for a boy to help them with the farm work, but instead, a thin, red-haired girl with big eyes stood before them."""
    st.markdown(f"<p style='line-height: 1.8; font-size: 16px;'>{english_paragraph}</p>", unsafe_allow_html=True)

with st.expander("📝 点击展开「中文翻译」 | Click to Expand [Chinese Translation]", expanded=True):
    chinese_paragraph = """安妮·雪莉并不是卡斯伯特兄妹所期待的那样。
他们本来申请了一个男孩来帮忙打理农场的活计，可站在他们面前的，却是一个瘦小、红头发、有着一双大眼睛的女孩。"""
    st.markdown(f"<p style='line-height: 1.8; font-size: 16px; color: #333;'>{chinese_paragraph}</p>", unsafe_allow_html=True)

st.markdown("---")

# 第二部分：小思考问题
st.header("🤔 小思考问题 | Little Thinking Questions")
questions = ["1. What did the Cuthberts want at first? （卡斯伯特兄妹一开始想要什么？）"]
for q in questions:
    st.write(f"✅ {q}")

st.markdown("---")

# 第三部分：互动游戏
st.header("🎮 单词配对小游戏 | Word Matching Game")
st.success("💡 游戏规则：用鼠标在单词和对应释义之间画线配对")
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0.0)",
    stroke_width=3,
    stroke_color="#1E90FF",
    background_color="#f0f8ff",
    height=200,
    width=600,
    drawing_mode="freedraw",
    key="canvas",
)

# 底部结束语
st.markdown("<h3 style='text-align: center;'>🌟 下次我们一起阅读更多有趣的故事吧！ | Let's read more interesting stories next time!</h3>", unsafe_allow_html=True)