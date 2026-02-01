import streamlit as st

# --------------------------
# 核心配置：隐藏侧边栏 + 儿童友好样式
# --------------------------
st.set_page_config(page_title="夏洛的网 | 双语阅读小屋", layout="wide")
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp {background-color: #FFF5E1;}
        h1 {color: #E67E22; text-align: center; font-size: 32px !important;}
        .stButton > button {background-color: #F39C12; color: white; font-size: 16px !important; border-radius: 8px; margin: 0 4px;}
        .feedback-audio {display: none !important; visibility: hidden !important; height: 0px !important; width: 0px !important;}
    </style>
""", unsafe_allow_html=True)

# --------------------------
# 音频配置
# --------------------------
english_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/夏洛的网_english.mp3"
chinese_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/夏洛的网_chinese.mp3"
correct_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/correct.mp3"
wrong_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/wrong.mp3"

# --------------------------
# 页面内容
# --------------------------
st.title("夏洛的网 / Charlotte's Web")

# 中英文段落
st.markdown("### 📖 经典段落")
st.markdown("**中文**：在朱克曼家的谷仓里，快乐地生活着一群动物。小猪威尔伯和蜘蛛夏洛建立了最真挚的友谊。然而，一个坏消息打破了谷仓的平静：威尔伯未来的命运竟是成为熏肉火腿。")
st.markdown("**English**：In the barn at Zuckerman's farm, a group of animals lived happily. Pig Wilbur and spider Charlotte formed the most sincere friendship. However, bad news broke the peace: Wilbur's future fate was to become bacon and ham.")

# 音频播放区
st.markdown("### 🎧 语音朗读")
st.audio(english_audio_url, format="audio/mp3")
st.caption("英文语音朗读")
st.audio(chinese_audio_url, format="audio/mp3")
st.caption("中文语音朗读")

# 隐藏的反馈音频（答题提示音）
st.audio(correct_audio_url, format="audio/mp3", loop=False, autoplay=False, key="correct_audio", css_class="feedback-audio")
st.audio(wrong_audio_url, format="audio/mp3", loop=False, autoplay=False, key="wrong_audio", css_class="feedback-audio")

# --------------------------
# 互动选择题
# --------------------------
st.markdown("### 🎯 小测试")

# 题目1
q1 = st.radio(
    "1. 威尔伯和谁建立了真挚的友谊？",
    ["A. 老鼠坦普尔顿", "B. 蜘蛛夏洛", "C. 小羊羔", "D. 鹅妈妈"],
    horizontal=True,
    key="q1"
)
if q1 == "B. 蜘蛛夏洛":
    st.success("✅ 答对啦！")
    st.markdown(f'<audio src="{correct_audio_url}" autoplay class="feedback-audio">', unsafe_allow_html=True)
elif q1 != "":
    st.error("❌ 再想想哦")
    st.markdown(f'<audio src="{wrong_audio_url}" autoplay class="feedback-audio">', unsafe_allow_html=True)

# 题目2
q2 = st.radio(
    "2. 威尔伯的命运原本是什么？",
    ["A. 成为宠物", "B. 参加比赛", "C. 成为熏肉火腿", "D. 被送走"],
    horizontal=True,
    key="q2"
)
if q2 == "C. 成为熏肉火腿":
    st.success("✅ 答对啦！")
    st.markdown(f'<audio src="{correct_audio_url}" autoplay class="feedback-audio">', unsafe_allow_html=True)
elif q2 != "":
    st.error("❌ 再想想哦")
    st.markdown(f'<audio src="{wrong_audio_url}" autoplay class="feedback-audio">', unsafe_allow_html=True)

# 题目3
q3 = st.radio(
    "3. 故事发生在哪个地方？",
    ["A. 森林里", "B. 朱克曼家的谷仓", "C. 农场主的房子", "D. 学校"],
    horizontal=True,
    key="q3"
)
if q3 == "B. 朱克曼家的谷仓":
    st.success("✅ 答对啦！")
    st.markdown(f'<audio src="{correct_audio_url}" autoplay class="feedback-audio">', unsafe_allow_html=True)
elif q3 != "":
    st.error("❌ 再想想哦")
    st.markdown(f'<audio src="{wrong_audio_url}" autoplay class="feedback-audio">', unsafe_allow_html=True)

# 题目4
q4 = st.radio(
    "4. 夏洛是什么动物？",
    ["A. 小猪", "B. 老鼠", "C. 蜘蛛", "D. 鹅"],
    horizontal=True,
    key="q4"
)
if q4 == "C. 蜘蛛":
    st.success("✅ 答对啦！")
    st.markdown(f'<audio src="{correct_audio_url}" autoplay class="feedback-audio">', unsafe_allow_html=True)
elif q4 != "":
    st.error("❌ 再想想哦")
    st.markdown(f'<audio src="{wrong_audio_url}" autoplay class="feedback-audio">', unsafe_allow_html=True)