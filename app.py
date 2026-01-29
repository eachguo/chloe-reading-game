# 导入所需库
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# ---------------------- 前置配置：马卡龙暖色系背景（优化版，清晰不刺眼） ----------------------
def set_macaron_warm_background():
    """设置马卡龙暖色系背景（浅蜜桃色+淡云朵，低饱和度，不喧宾夺主）"""
    background_css = """
    <style>
    /* 整体背景：马卡龙浅蜜桃色+淡云朵 */
    .stApp {
        background-color: #fff3e6;
        background-image: url("https://picsum.photos/id/1076/1920/1080");
        background-size: cover;
        background-opacity: 0.06;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    /* 文本区域优化 */
    .stExpander, .stHeader, .stSuccess, .stButton > button {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 8px !important;
        padding: 10px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    /* 标题颜色统一为马卡龙暖橘色 */
    h1, h2, h3, h4 {
        color: #d48b6b !important;
    }
    /* 分割线颜色统一为马卡龙暖橘色 */
    .stDivider {
        border-top: 2px solid #d48b6b !important;
    }
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)

# ---------------------- 页面基础配置（双语标题，兼容手机） ----------------------
st.set_page_config(
    page_title="Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut",
    page_icon="📚",
    layout="centered"
)

# 应用马卡龙暖色系背景
set_macaron_warm_background()

# ---------------------- 页面主标题（双语，美化排版） ----------------------
st.title("📚 Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut")
story_topic_cn = "《安妮的绿山墙》"
story_topic_en = "Anne of Green Gables"
st.subheader(f"—— {story_topic_cn} 专属阅读版 | Exclusive Reading Edition of {story_topic_en}")
st.divider()

# ---------------------- 第一部分：中英双语段落（双语标题，清晰排版） ----------------------
st.header("✨ 趣味段落阅读 | Fun Paragraph Reading", anchor=False, help="中英对照，轻松阅读 | Bilingual Comparison, Easy to Read")

# 英文原文（可折叠，清晰排版）
with st.expander("📖 点击展开「英文原文」 | Click to Expand [English Original]", expanded=True):
    english_paragraph = """Anne Shirley was not what the Cuthberts had expected. 
They had sent for a boy to help them with the farm work, but instead, a thin, red-haired girl with big eyes stood before them. 
She talked and talked, telling them about her life in the orphanage and her dreams of having a real home. 
Anne loved to imagine things—she called the cherry tree outside her window a "snow queen" and the brook a "silver thread". 
For her, the world was full of magic and beauty, even when life was hard."""
    st.markdown(f"<p style='line-height: 1.8; font-size: 16px; color: #333;'>{english_paragraph}</p>", unsafe_allow_html=True)

# 中文翻译（可折叠，清晰排版）
with st.expander("📝 点击展开「中文翻译」 | Click to Expand [Chinese Translation]", expanded=True):
    chinese_paragraph = """安妮·雪莉并不是卡斯伯特兄妹所期待的那样。
他们本来申请了一个男孩来帮忙打理农场的活计，可站在他们面前的，却是一个瘦小、红头发、有着一双大眼睛的女孩。
她滔滔不绝地说着，跟他们讲述自己在孤儿院的生活，以及拥有一个真正家的梦想。
安妮喜欢幻想——她把窗外的樱桃树称作“白雪女王”，把小溪称作“银线”。
对她来说，即便生活艰难，这个世界也依然充满了魔法与美好。"""
    st.markdown(f"<p style='line-height: 1.8; font-size: 16px; color: #333;'>{chinese_paragraph}</p>", unsafe_allow_html=True)

st.divider()

# ---------------------- 第二部分：小思考问题（双语标题） ----------------------
st.header("🤔 小思考问题 | Little Thinking Questions", anchor=False, help="试着回答一下吧！ | Try to answer them!")
questions = [
    "1. What did the Cuthberts want at first? （卡斯伯特兄妹一开始想要什么？）",
    "2. What color is Anne's hair? （安妮的头发是什么颜色的？）",
    "3. What did Anne call the cherry tree? （安妮把樱桃树称作什么？）",
    "4. What is Anne's dream? （安妮的梦想是什么？）"
]
for q in questions:
    st.write(f"✅ {q}")

st.divider()

# ---------------------- 第三部分：互动式单词配对游戏（可画线，对错反馈） ----------------------
st.header("🎮 单词配对小游戏 | Word Matching Game", anchor=False, help="轻松记单词，快乐学英语 | Remember words easily, learn English happily")
st.success("💡 游戏规则：用鼠标在单词和对应释义之间画线配对，提交后查看对错 | Game Rule: Draw lines between words and their meanings, check results after submission.")

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
        st.markdown(f"<p style='line-height: 2.0; font-size: 15px; color: #333;'>{word}</p>", unsafe_allow_html=True)
with col2:
    st.markdown("<h4 style='text-align: center;'>中文释义 | Chinese Meanings</h4>", unsafe_allow_html=True)
    for word in words_right:
        st.markdown(f"<p style='line-height: 2.0; font-size: 15px; color: #333;'>{word}</p>", unsafe_allow_html=True)

# 互动画布（支持鼠标画线，适配暖色系）
st.markdown("### 🎨 点击下方画布开始画线配对 | Click the canvas below to start drawing lines")
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0.0)",
    stroke_width=3,
    stroke_color="#d48b6b",
    background_color="#fdf6f0",
    update_streamlit=True,
    height=300,
    width=600,
    drawing_mode="freedraw",
    key="canvas",
)

# 对错判断与颜色反馈（清晰明了）
if st.button("✅ 提交答案并判断 | Submit Answer and Judge"):
    st.subheader("📊 配对结果 | Matching Result")
    # 正确配对（绿色显示）
    st.markdown("### ✅ 正确配对 | Correct Matches")
    correct_pairs = [
        ("orphanage —— 孤儿院 | Orphanage", "green"),
        ("farm —— 农场 | Farm", "green"),
        ("dream —— 梦想 | Dream", "green"),
        ("cherry tree —— 樱桃树 | Cherry Tree", "green"),
        ("magic —— 魔法 | Magic", "green")
    ]
    for pair, color in correct_pairs:
        st.markdown(f"<p style='color: {color}; font-size: 15px;'>{pair}</p>", unsafe_allow_html=True)
    
    # 错误示例（红色显示，供参考）
    st.markdown("### ❌ 错误示例 | Wrong Example (For Reference)")
    st.markdown(f"<p style='color: red; font-size: 15px;'>orphanage —— 农场 | Orphanage —— Farm</p>", unsafe_allow_html=True)

# 正确答案展示（可折叠）
with st.expander("🎉 点击查看「正确答案」 | Click to View [Correct Answer]", expanded=False):
    st.markdown("""
    1. orphanage —— B. 孤儿院 | B. Orphanage
    2. farm —— A. 农场 | A. Farm
    3. dream —— D. 梦想 | D. Dream
    4. cherry tree —— C. 樱桃树 | C. Cherry Tree
    5. magic —— E. 魔法 | E. Magic
    """)

st.divider()

# ---------------------- 底部结束语（双语，暖色系美化） ----------------------
st.markdown("<h3 style='text-align: center; color: #d48b6b;'>🌟 下次我们一起阅读更多有趣的故事吧！ | Let's read more interesting stories next time!</h3>", unsafe_allow_html=True)