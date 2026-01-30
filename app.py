# 导入必备库（仅保留核心依赖，无冗余，确保兼容）
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
    .stExpander, .stHeader, .stSuccess, .stButton > button, .stTextInput > div > div {
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

# ---------------------- 核心功能：完整双语内容 + 新手友好单词配对 ----------------------
st.title("Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut")
story_topic_cn = "《安妮的绿山墙》"
story_topic_en = "Anne of Green Gables"
st.subheader(f"—— {story_topic_cn} 专属阅读版 | Exclusive Reading Edition of {story_topic_en}")
st.divider()

# 中英双语段落（完整内容，无节选）
st.header("趣味段落阅读 | Fun Paragraph Reading")
with st.expander("点击展开「英文原文」 | Click to Expand [English Original]", expanded=True):
    english_paragraph = """Anne Shirley was not what the Cuthberts had expected. They had sent for a boy to help them with the farm work, but instead, a thin, red-haired girl with big eyes stood before them. She talked and talked, telling them about her life in the orphanage and her dreams of having a real home. Anne loved to imagine things—she called the cherry tree outside her window a "snow queen" and the brook a "silver thread". For her, the world was full of magic and beauty, even when life was hard. She hoped that the Cuthberts would keep her and that she would finally have a place to call home."""
    st.write(english_paragraph)

with st.expander("点击展开「中文翻译」 | Click to Expand [Chinese Translation]", expanded=True):
    chinese_paragraph = """安妮·雪莉并不是卡斯伯特兄妹所期待的那样。他们本来申请了一个男孩来帮忙打理农场的活计，可站在他们面前的，却是一个瘦小、红头发、有着一双大眼睛的女孩。她滔滔不绝地说着，跟他们讲述自己在孤儿院的生活，以及拥有一个真正家的梦想。安妮喜欢幻想——她把窗外的樱桃树称作“白雪女王”，把小溪称作“银线”。对她来说，即便生活艰难，这个世界也依然充满了魔法与美好。她希望卡斯伯特兄妹能留下她，希望自己终于能有一个可以称之为“家”的地方。"""
    st.write(chinese_paragraph)

st.divider()

# 小思考问题（完整列表）
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

# ---------------------- 单词配对小游戏（新手友好版：手绘连线+手动输入+对错判断） ----------------------
st.header("单词配对小游戏 | Word Matching Game")
st.success("游戏规则：1. 对着下方单词在画布手绘连线；2. 输入你的答案（格式示例：1B,2A,3D,4C）；3. 提交查看对错")

# 第一步：展示单词列表（左右对齐，对应画布视觉关联）
st.write("### 单词对应列表")
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

# 第二步：手绘画布（加宽，方便对应两侧单词，保留暖色系风格）
st.write("### 请在下方画布手绘连线配对")
canvas_result = st_canvas(
    fill_color="rgba(255,255,255,0)",  # 透明填充，只保留手绘线条
    stroke_width=3,
    stroke_color="#d48b6b",  # 马卡龙暖橘色线条，呼应整体风格
    background_color="#fdf6f0",  # 浅于主背景，清晰可见
    height=300,  # 高度足够，方便绘制多条连线
    width=700,  # 加宽画布，对应两侧单词的间距
    drawing_mode="freedraw",
    key="canvas",
)

# 第三步：手动输入答案（输入框，给出明确格式提示）
user_answer = st.text_input(
    label="请输入你的配对答案（严格按照格式：1B,2A,3D,4C）",
    placeholder="例如：1B,2A,3D,4C",
    help="请不要修改格式，直接替换对应字母即可"
)

# 第四步：提交答案+对错判断（闭环逻辑，友好反馈）
if st.button("提交答案并查看正确结果 | Submit Answer and Check Correct Results"):
    # 预设正确答案（固定格式，与输入框对应）
    correct_answer = "1B,2A,3D,4C"
    # 详细配对结果，方便展示
    correct_pair_detail = {
        "1. orphanage": "B. 孤儿院",
        "2. farm": "A. 农场",
        "3. dream": "D. 梦想",
        "4. cherry tree": "C. 樱桃树"
    }
    
    # 第一步：展示完整正确答案
    st.write("### 📌 完整正确配对答案")
    for word, meaning in correct_pair_detail.items():
        st.write(f"{word} → {meaning}")
    
    # 第二步：简单判断对错（忽略空格、大小写，提升用户体验）
    # 清理用户输入和正确答案（去除空格，转为大写，避免格式小误差导致误判）
    user_answer_clean = user_answer.replace(" ", "").upper()
    correct_answer_clean = correct_answer.replace(" ", "").upper()
    
    # 分情况反馈
    if user_answer == "":
        st.warning("⚠️ 请先在输入框中输入你的答案哦！")
    elif user_answer_clean == correct_answer_clean:
        st.success("🎉 太棒了！全部答对了，你太优秀了！")
    else:
        st.error("❌ 答案有误，再对照正确答案仔细核对一下吧！")

st.divider()

# 底部结束语
st.write("### 下次我们一起阅读更多有趣的故事吧！ | Let's read more interesting stories next time!")