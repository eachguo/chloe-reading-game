import streamlit as st
import streamlit.components.v1 as components

# --------------------------
# 核心配置：1:1复刻《安妮的绿山墙》
# --------------------------
st.set_page_config(page_title="夏洛的网 | 双语阅读小屋", layout="wide")
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp {background-color: #FFF5E1;}
        h1 {
            color: #E67E22; 
            text-align: center; 
            font-size: 36px !important;
            font-weight: bold;
            margin: 20px 0;
        }
        h3 {
            color: #D35400;
            font-size: 24px !important;
            font-weight: bold;
            margin: 20px 0;
        }
        h4 {
            color: #E67E22;
            font-size: 20px !important;
            font-weight: bold;
            margin: 15px 0;
        }
        p, .stMarkdown, .stButton {
            font-size: 18px !important;
            color: #5D4037;
            line-height: 1.6;
        }
        .stButton > button {
            background-color: #FFFFFF;
            color: #D35400;
            border: 1px solid #F39C12;
            font-size: 18px !important;
            border-radius: 8px;
            margin: 0 8px;
            padding: 8px 16px;
            font-weight: 500;
        }
        .stButton > button:hover {
            background-color: #FFF9E8;
            border-color: #E67E22;
        }
        .hidden-audio {display: none !important;}
        .quiz-section {margin: 25px 0; padding: 20px; border-radius: 12px; background-color: #FFF9E8;}
        .end-note {
            text-align: center;
            margin-top: 50px;
            padding: 25px;
            border-top: 2px solid #F39C12;
            color: #D35400;
            font-size: 20px !important;
            font-weight: bold;
        }
        .question-title {
            margin: 10px 0 20px 0;
            color: #5D4037;
            font-size: 19px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# 音频配置：复用《安妮的绿山墙》稳定逻辑
# --------------------------
english_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/夏洛的网_english.mp3"
chinese_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/夏洛的网_chinese.mp3"
correct_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/correct.mp3"
wrong_audio_url = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/wrong.mp3"

# 嵌入和《安妮的绿山墙》完全一致的音频播放器（确保提示音正常）
components.html(f"""
    <audio id="correct-audio" src="{correct_audio_url}" preload="auto">
    <audio id="wrong-audio" src="{wrong_audio_url}" preload="auto">
    <script>
        // 绑定用户交互，避免浏览器拦截音频播放
        window.addEventListener('click', function() {{
            // 预加载音频，确保首次点击就能播放
            const correctAudio = document.getElementById('correct-audio');
            const wrongAudio = document.getElementById('wrong-audio');
            correctAudio.load();
            wrongAudio.load();
        }}, {{ once: true }});
        
        // 正确提示音播放函数
        function playCorrectSound() {{
            const audio = document.getElementById('correct-audio');
            audio.currentTime = 0; // 重置播放进度
            audio.play().then(() => {{}}).catch(e => console.log('正确提示音播放:', e));
        }}
        
        // 错误提示音播放函数
        function playWrongSound() {{
            const audio = document.getElementById('wrong-audio');
            audio.currentTime = 0; // 重置播放进度
            audio.play().then(() => {{}}).catch(e => console.log('错误提示音播放:', e));
        }}
    </script>
""", height=0)

# --------------------------
# 页面内容：格式、字体完全对齐《安妮的绿山墙》
# --------------------------
st.title("夏洛的网 / Charlotte's Web")

st.markdown("### 📖 经典段落 / Classic Passage")
st.markdown("**中文**：在朱克曼家的谷仓里，快乐地生活着一群动物。小猪威尔伯刚来到这里时，觉得孤单又害怕，直到它遇见了蜘蛛夏洛。夏洛就住在谷仓门框的角落，它用丝线织出漂亮的网，还会给威尔伯讲夜晚的故事。\n\n它们很快成了最好的朋友。然而，一个坏消息打破了谷仓的平静：农场主计划在圣诞节把威尔伯杀掉，做成熏肉火腿。威尔伯绝望地哭了起来，夏洛温柔地安慰它：“别害怕，我会救你的。”")
st.markdown("**English**：In the barn at Zuckerman's farm, a group of animals lived happily. When Wilbur the pig first arrived, he felt lonely and scared—until he met Charlotte the spider. Charlotte lived in the corner of the barn doorframe, weaving beautiful webs with her silk and telling Wilbur stories of the night.\n\nThey soon became best friends. However, bad news shattered the barn's peace: the farmer planned to kill Wilbur at Christmas and turn him into bacon and ham. Wilbur cried in despair, but Charlotte comforted him gently: \"Don't worry, I will save you.\"")

# 音频播放区：和《安妮的绿山墙》布局一致
st.markdown("### 🎧 语音朗读 / Audio Reading")
st.audio(english_audio_url, format="audio/mp3")
st.caption("英文语音朗读 / English Audio")
st.audio(chinese_audio_url, format="audio/mp3")
st.caption("中文语音朗读 / Chinese Audio")

# --------------------------
# 互动选择题：按钮式交互，1:1复刻《安妮的绿山墙》
# --------------------------
st.markdown("### 🎯 小测试 / Mini Quiz")
st.markdown("💡 点击你认为正确的选项，自动播放提示音哦！/ Click the option you think is correct, and a prompt sound will play automatically!")

# --- 题目1 ---
st.markdown("<div class='question-title'>1. 小猪威尔伯刚到谷仓时，心情是怎样的？ / How did Wilbur feel when he first arrived at the barn?</div>", unsafe_allow_html=True)
col1_1, col1_2, col1_3, col1_4 = st.columns(4)
with col1_1:
    if st.button("A. 开心又兴奋 / Happy and excited", key="q1_a"):
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrongSound();</script>", height=0)
with col1_2:
    if st.button("B. 孤单又害怕 / Lonely and scared", key="q1_b"):
        st.success("✅ 答对啦！太棒了！/ Correct! You're amazing!")
        components.html("<script>playCorrectSound();</script>", height=0)
with col1_3:
    if st.button("C. 愤怒又暴躁 / Angry and grumpy", key="q1_c"):
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrongSound();</script>", height=0)
with col1_4:
    if st.button("D. 平静又淡然 / Calm and indifferent", key="q1_d"):
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrongSound();</script>", height=0)

st.divider() # 分隔线，和《安妮的绿山墙》一致

# --- 题目2 ---
st.markdown("<div class='question-title'>2. 夏洛住在谷仓的哪个位置？ / Where did Charlotte live in the barn?</div>", unsafe_allow_html=True)
col2_1, col2_2, col2_3, col2_4 = st.columns(4)
with col2_1:
    if st.button("A. 谷仓门框的角落 / Corner of the barn doorframe", key="q2_a"):
        st.success("✅ 答对啦！太棒了！/ Correct! You're amazing!")
        components.html("<script>playCorrectSound();</script>", height=0)
with col2_2:
    if st.button("B. 干草堆上 / On the haystack", key="q2_b"):
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrongSound();</script>", height=0)
with col2_3:
    if st.button("C. 猪栏旁边 / Next to the pigpen", key="q2_c"):
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrongSound();</script>", height=0)
with col2_4:
    if st.button("D. 窗户边 / By the window", key="q2_d"):
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrongSound();</script>", height=0)

st.divider()

# --- 题目3 ---
st.markdown("<div class='question-title'>3. 农场主计划在什么时候杀掉威尔伯？ / When did the farmer plan to kill Wilbur?</div>", unsafe_allow_html=True)
col3_1, col3_2, col3_3, col3_4 = st.columns(4)
with col3_1:
    if st.button("A. 春节 / Spring Festival", key="q3_a"):
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrongSound();</script>", height=0)
with col3_2:
    if st.button("B. 国庆节 / National Day", key="q3_b"):
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrongSound();</script>", height=0)
with col3_3:
    if st.button("C. 圣诞节 / Christmas", key="q3_c"):
        st.success("✅ 答对啦！太棒了！/ Correct! You're amazing!")
        components.html("<script>playCorrectSound();</script>", height=0)
with col3_4:
    if st.button("D. 中秋节 / Mid-Autumn Festival", key="q3_d"):
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrongSound();</script>", height=0)

st.divider()

# --- 题目4 ---
st.markdown("<div class='question-title'>4. 夏洛对威尔伯说的安慰话是？ / What did Charlotte say to comfort Wilbur?</div>", unsafe_allow_html=True)
col4_1, col4_2, col4_3, col4_4 = st.columns(4)
with col4_1:
    if st.button("A. 别害怕，我会救你的 / Don't worry, I will save you", key="q4_a"):
        st.success("✅ 答对啦！太棒了！/ Correct! You're amazing!")
        components.html("<script>playCorrectSound();</script>", height=0)
with col4_2:
    if st.button("B. 别哭了，没人能帮你 / Stop crying, no one can help you", key="q4_b"):
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrongSound();</script>", height=0)
with col4_3:
    if st.button("C. 勇敢点，接受命运吧 / Be brave and accept your fate", key="q4_c"):
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrongSound();</script>", height=0)
with col4_4:
    if st.button("D. 加油，你可以逃跑的 / Come on, you can run away", key="q4_d"):
        st.error("❌ 再想想哦！/ Try again!")
        components.html("<script>playWrongSound();</script>", height=0)

# --------------------------
# 结尾文案：1:1复刻《安妮的绿山墙》
# --------------------------
st.markdown("""
    <div class="end-note">
        ✨ 下次我们一起阅读更多有趣的故事吧！ | Let's read more interesting stories next time!
    </div>
""", unsafe_allow_html=True)