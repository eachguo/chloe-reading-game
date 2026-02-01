import streamlit as st
import streamlit.components.v1 as components

# --------------------------
# 核心配置：完全对齐《安妮的绿山墙》
# --------------------------
st.set_page_config(page_title="夏洛的网 | 双语阅读小屋", layout="wide")
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp {background-color: #FFF5E1;}
        h1 {color: #E67E22; text-align: center; font-size: 32px !important;}
        h3 {color: #D35400;}
        h4 {color: #E67E22;}
        .stButton > button {
            background-color: #FFFFFF;
            color: #D35400;
            border: 1px solid #F39C12;
            font-size: 16px !important;
            border-radius: 8px;
            margin: 0 4px;
            padding: 6px 12px;
        }
        .stButton > button:hover {
            background-color: #FFF9E8;
        }
        .hidden-audio {display: none !important;}
        .quiz-section {margin: 20px 0; padding: 15px; border-radius: 10px; background-color: #FFF9E8;}
        .end-note {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            border-top: 1px solid #F39C12;
            color: #D35400;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# 音频配置
# --------------------------
english_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/夏洛的网_english.mp3"
chinese_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/夏洛的网_chinese.mp3"
correct_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/correct.mp3"
wrong_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/wrong.mp3"

# 嵌入和《安妮的绿山墙》完全一致的音频播放器
components.html(f"""
    <audio id="correct-audio" src="{correct_audio_url}" preload="auto">
    <audio id="wrong-audio" src="{wrong_audio_url}" preload="auto">
    <script>
        function playCorrect() {{
            const audio = document.getElementById('correct-audio');
            audio.currentTime = 0;
            audio.play().catch(e => console.log('播放失败:', e));
        }}
        function playWrong() {{
            const audio = document.getElementById('wrong-audio');
            audio.currentTime = 0;
            audio.play().catch(e => console.log('播放失败:', e));
        }}
    </script>
""", height=0)

# --------------------------
# 页面内容
# --------------------------
st.title("夏洛的网 / Charlotte's Web")

st.markdown("### 📖 经典段落 / Classic Passage")
st.markdown("**中文**：在朱克曼家的谷仓里，快乐地生活着一群动物。小猪威尔伯刚来到这里时，觉得孤单又害怕，直到它遇见了蜘蛛夏洛。夏洛就住在谷仓门框的角落，它用丝线织出漂亮的网，还会给威尔伯讲夜晚的故事。\n\n它们很快成了最好的朋友。然而，一个坏消息打破了谷仓的平静：农场主计划在圣诞节把威尔伯杀掉，做成熏肉火腿。威尔伯绝望地哭了起来，夏洛温柔地安慰它：“别害怕，我会救你的。”")
st.markdown("**English**：In the barn at Zuckerman's farm, a group of animals lived happily. When Wilbur the pig first arrived, he felt lonely and scared—until he met Charlotte the spider. Charlotte lived in the corner of the barn doorframe, weaving beautiful webs with her silk and telling Wilbur stories of the night.\n\nThey soon became best friends. However, bad news shattered the barn's peace: the farmer planned to kill Wilbur at Christmas and turn him into bacon and ham. Wilbur cried in despair, but Charlotte comforted him gently: \"Don't worry, I will save you.\"")

# 音频播放区
st.markdown("### 🎧 语音朗读 / Audio Reading")
st.audio(english_audio_url, format="audio/mp3")
st.caption("英文语音朗读 / English Audio")
st.audio(chinese_audio_url, format="audio/mp3")
st.caption("中文语音朗读 / Chinese Audio")

# --------------------------
# 互动选择题（完全对齐《安妮的绿山墙》）
# --------------------------
st.markdown("### 🎯 小测试 / Mini Quiz")
st.markdown("💡 点击你认为正确的选项，自动播放提示音哦！/ Click the option you think is correct, and a prompt sound will play automatically!")

# 题目1
with st.container():
    st.markdown("#### 1. 小猪威尔伯刚到谷仓时，心情是怎样的？ / How did Wilbur feel when he first arrived at the barn?")
    q1 = st.radio(
        "",
        ["A. 开心又兴奋 / Happy and excited", "B. 孤单又害怕 / Lonely and scared", "C. 愤怒又暴躁 / Angry and grumpy", "D. 平静又淡然 / Calm and indifferent"],
        horizontal=True,
        key="q1",
        index=None
    )
    if q1 == "B. 孤单又害怕 / Lonely and scared":
        st.success("✅ 答对啦！太棒了！/ Correct! You're amazing!")
        components.html("<script>playCorrect()</script>", height=0)
    elif q1 is not None and q1 != "B. 孤单又害怕 / Lonely and scared":
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrong()</script>", height=0)

# 题目2
with st.container():
    st.markdown("#### 2. 夏洛住在谷仓的哪个位置？ / Where did Charlotte live in the barn?")
    q2 = st.radio(
        "",
        ["A. 谷仓门框的角落 / Corner of the barn doorframe", "B. 干草堆上 / On the haystack", "C. 猪栏旁边 / Next to the pigpen", "D. 窗户边 / By the window"],
        horizontal=True,
        key="q2",
        index=None
    )
    if q2 == "A. 谷仓门框的角落 / Corner of the barn doorframe":
        st.success("✅ 答对啦！太棒了！/ Correct! You're amazing!")
        components.html("<script>playCorrect()</script>", height=0)
    elif q2 is not None and q2 != "A. 谷仓门框的角落 / Corner of the barn doorframe":
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrong()</script>", height=0)

# 题目3
with st.container():
    st.markdown("#### 3. 农场主计划在什么时候杀掉威尔伯？ / When did the farmer plan to kill Wilbur?")
    q3 = st.radio(
        "",
        ["A. 春节 / Spring Festival", "B. 国庆节 / National Day", "C. 圣诞节 / Christmas", "D. 中秋节 / Mid-Autumn Festival"],
        horizontal=True,
        key="q3",
        index=None
    )
    if q3 == "C. 圣诞节 / Christmas":
        st.success("✅ 答对啦！太棒了！/ Correct! You're amazing!")
        components.html("<script>playCorrect()</script>", height=0)
    elif q3 is not None and q3 != "C. 圣诞节 / Christmas":
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrong()</script>", height=0)

# 题目4
with st.container():
    st.markdown("#### 4. 夏洛对威尔伯说的安慰话是？ / What did Charlotte say to comfort Wilbur?")
    q4 = st.radio(
        "",
        ["A. 别害怕，我会救你的 / Don't worry, I will save you", "B. 别哭了，没人能帮你 / Stop crying, no one can help you", "C. 勇敢点，接受命运吧 / Be brave and accept your fate", "D. 加油，你可以逃跑的 / Come on, you can run away"],
        horizontal=True,
        key="q4",
        index=None
    )
    if q4 == "A. 别害怕，我会救你的 / Don't worry, I will save you":
        st.success("✅ 答对啦！太棒了！/ Correct! You're amazing!")
        components.html("<script>playCorrect()</script>", height=0)
    elif q4 is not None and q4 != "A. 别害怕，我会救你的 / Don't worry, I will save you":
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrong()</script>", height=0)

# --------------------------
# 结尾文案：完全对齐《安妮的绿山墙》
# --------------------------
st.markdown("""
    <div class="end-note">
        ✨ 下次我们一起阅读更多有趣的故事吧！ | Let's read more interesting stories next time!
    </div>
""", unsafe_allow_html=True)