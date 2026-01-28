# 导入Streamlit库，用于快速构建网页应用
import streamlit as st

# ---------------------- 页面基础配置（固定不变，美化外观） ----------------------
st.set_page_config(
    page_title="Chloe's 双语阅读小屋",  # 页面标题（浏览器标签显示）
    page_icon="📚",  # 页面小图标（书本图标，更可爱）
    layout="centered"  # 页面内容居中显示，适合小朋友观看
)

# ---------------------- 页面标题与样式（固定不变，美化外观） ----------------------
st.title("📚 Chloe's 双语阅读小屋")
st.subheader("—— 《安妮的绿山墙》专属阅读版", divider="green")
st.markdown("---")  # 分隔线，让排版更整洁

# ---------------------- 第一部分：中英双语趣味段落（核心内容，后续可直接替换） ----------------------
st.header("✨ 趣味段落阅读", anchor=False, help="中英对照，轻松阅读")

# 英文原文
with st.expander("📖 点击展开「英文原文」", expanded=True):  # 可折叠面板，更灵活
    english_paragraph = """Anne Shirley was not what the Cuthberts had expected. 
They had sent for a boy to help them with the farm work, but instead, a thin, red-haired girl with big eyes stood before them. 
She talked and talked, telling them about her life in the orphanage and her dreams of having a real home. 
Anne loved to imagine things—she called the cherry tree outside her window a "snow queen" and the brook a "silver thread". 
For her, the world was full of magic and beauty, even when life was hard."""
    st.markdown(f"<p style='line-height: 1.8; font-size: 16px;'>{english_paragraph}</p>", unsafe_allow_html=True)

# 中文翻译
with st.expander("📝 点击展开「中文翻译」", expanded=True):
    chinese_paragraph = """安妮·雪莉并不是卡斯伯特兄妹所期待的那样。
他们本来申请了一个男孩来帮忙打理农场的活计，可站在他们面前的，却是一个瘦小、红头发、有着一双大眼睛的女孩。
她滔滔不绝地说着，跟他们讲述自己在孤儿院的生活，以及拥有一个真正家的梦想。
安妮喜欢幻想——她把窗外的樱桃树称作“白雪女王”，把小溪称作“银线”。
对她来说，即便生活艰难，这个世界也依然充满了魔法与美好。"""
    st.markdown(f"<p style='line-height: 1.8; font-size: 16px; color: #333;'>{chinese_paragraph}</p>", unsafe_allow_html=True)

st.markdown("---")  # 分隔线

# ---------------------- 第二部分：小思考问题（核心内容，后续可直接替换） ----------------------
st.header("🤔 小思考问题", anchor=False, help="试着回答一下吧！")
questions = [
    "1. What did the Cuthberts want at first? （卡斯伯特兄妹一开始想要什么？）",
    "2. What color is Anne's hair? （安妮的头发是什么颜色的？）",
    "3. What did Anne call the cherry tree? （安妮把樱桃树称作什么？）",
    "4. What is Anne's dream? （安妮的梦想是什么？）"
]
for q in questions:
    st.write(f"✅ {q}")

st.markdown("---")  # 分隔线

# ---------------------- 第三部分：单词配对小游戏（核心内容，后续可直接替换） ----------------------
st.header("🎮 单词配对小游戏", anchor=False, help="轻松记单词，快乐学英语")
st.success("💡 游戏规则：把左边的英文单词和右边的中文意思对应起来哦！")

# 游戏内容
game_content = """
1. orphanage —— A. 农场
2. farm —— B. 孤儿院
3. dream —— D. 梦想
4. cherry tree —— C. 樱桃树
5. magic —— E. 魔法
"""
st.markdown(f"<p style='line-height: 2.0; font-size: 15px; background-color: #f0f8ff; padding: 15px; border-radius: 8px;'>{game_content}</p>", unsafe_allow_html=True)

# 答案揭晓（可折叠，增加互动性）
with st.expander("🎉 点击查看「正确答案」", expanded=False):
    st.markdown("""
    1. orphanage —— B. 孤儿院
    2. farm —— A. 农场
    3. dream —— D. 梦想
    4. cherry tree —— C. 樱桃树
    5. magic —— E. 魔法
    """)

# ---------------------- 底部结束语（固定不变，美化外观） ----------------------
st.markdown("---")
st.markdown("### 🌟 下次我们一起阅读更多有趣的故事吧！", text_align="center")