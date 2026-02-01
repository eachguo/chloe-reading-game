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
        h3 {color: #D35400;}
        .stButton > button {background-color: #F39C12; color: white; font-size: 16px !important; border-radius: 8px; margin: 0 4px;}
        /* 用key属性定位隐藏提示音播放器 */
        [data-testid="stAudio"][key="correct_audio"],
        [data-testid="stAudio"][key="wrong_audio"] {
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
            width: 0px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# 音频配置（已匹配你上传的音频文件名，无需修改）
# --------------------------
english_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/夏洛的网_english.mp3"
chinese_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/夏洛的网_chinese.mp3"
correct_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/correct.mp3"
wrong_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/wrong.mp3"

# --------------------------
# 页面内容（扩充版中英文段落，故事性更强）
# --------------------------
st.title("夏洛的网 / Charlotte's Web")

# 中英文段落（扩充版）
st.markdown("### 📖 经典段落")
st.markdown("**中文**：在朱克曼家的谷仓里，快乐地生活着一群动物。小猪威尔伯刚来到这里时，觉得孤单又害怕，直到它遇见了蜘蛛夏洛。夏洛就住在谷仓门框的角落，它用丝线织出漂亮的网，还会给威尔伯讲夜晚的故事。\n\n它们很快成了最好的朋友。然而，一个坏消息打破了谷仓的平静：农场主计划在圣诞节把威尔伯杀掉，做成熏肉火腿。威尔伯绝望地哭了起来，夏洛温柔地安慰它：“别害怕，我会救你的。”")
st.markdown("**English**：In the barn at Zuckerman's farm, a group of animals lived happily. When Wilbur the pig first arrived, he felt lonely and scared—until he met Charlotte the spider. Charlotte lived in the corner of the barn doorframe, weaving beautiful webs with her silk and telling Wilbur stories of the night.\n\nThey soon became best friends. However, bad news shattered the barn's peace: the farmer planned to kill Wilbur at Christmas and turn him into bacon and ham. Wilbur cried in despair, but Charlotte comforted him gently: \"Don't worry, I will save you.\"")

# 音频播放区
st.markdown("### 🎧 语音朗读")
st.audio(english_audio_url, format="audio/mp3")
st.caption("英文语音朗读")
st.audio(chinese_audio_url, format="audio/mp3")
st.caption("中文语音朗读")

# 隐藏的反馈音频（答题提示音，通过CSS隐藏）
st.audio(correct_audio_url, format="audio/mp3", loop=False, autoplay=False, key="correct_audio")
st.audio(wrong_audio_url, format="audio/mp3", loop=False, autoplay=False, key="wrong_audio")

# --------------------------
# 互动选择题（匹配扩充版段落，全局唯一key）
# --------------------------
st.markdown("### 🎯 小测试")

# 题目1
q1 = st.radio(
    "1. 小猪威尔伯刚到谷仓时，心情是怎样的？",
    ["A. 开心又兴奋", "B. 孤单又害怕", "C. 愤怒又暴躁", "D. 平静又淡然"],
    horizontal=True,
    key="q1"
)
if q1 == "B. 孤单又害怕":
    st.success("✅ 答对啦！")
    st.markdown(f'<audio src="{correct_audio_url}" autoplay>', unsafe_allow_html=True)
elif q1 != "":
    st.error("❌ 再想想哦")
    st.markdown(f'<audio src="{wrong_audio_url}" autoplay>', unsafe_allow_html=True)

# 题目2
q2 = st.radio(
    "2. 夏洛住在谷仓的哪个位置？",
    ["A. 谷仓门框的角落", "B. 干草堆上", "C. 猪栏旁边", "D. 窗户边"],
    horizontal=True,
    key="q2"
)
if q2 == "A. 谷仓门框的角落":
    st.success("✅ 答对啦！")
    st.markdown(f'<audio src="{correct_audio_url}" autoplay>', unsafe_allow_html=True)
elif q2 != "":
    st.error("❌ 再想想哦")
    st.markdown(f'<audio src="{wrong_audio_url}" autoplay>', unsafe_allow_html=True)

# 题目3
q3 = st.radio(
    "3. 农场主计划在什么时候杀掉威尔伯？",
    ["A. 春节", "B. 国庆节", "C. 圣诞节", "D. 中秋节"],
    horizontal=True,
    key="q3"
)
if q3 == "C. 圣诞节":
    st.success("✅ 答对啦！")
    st.markdown(f'<audio src="{correct_audio_url}" autoplay>', unsafe_allow_html=True)
elif q3 != "":
    st.error("❌ 再想想哦")
    st.markdown(f'<audio src="{wrong_audio_url}" autoplay>', unsafe_allow_html=True)

# 题目4
q4 = st.radio(
    "4. 夏洛对威尔伯说的安慰话是？",
    ["A. 别害怕，我会救你的", "B. 别哭了，没人能帮你", "C. 勇敢点，接受命运吧", "D. 加油，你可以逃跑的"],
    horizontal=True,
    key="q4"
)
if q4 == "A. 别害怕，我会救你的":
    st.success("✅ 答对啦！")
    st.markdown(f'<audio src="{correct_audio_url}" autoplay>', unsafe_allow_html=True)
elif q4 != "":
    st.error("❌ 再想想哦")
    st.markdown(f'<audio src="{wrong_audio_url}" autoplay>', unsafe_allow_html=True)