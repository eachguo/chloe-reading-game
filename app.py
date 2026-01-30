# 导入必备库
import streamlit as st
from io import BytesIO
import numpy as np
from scipy.io import wavfile

# ---------------------- 马卡龙纯色背景 + 隐藏音效播放器（核心优化） ----------------------
def set_macaron_warm_background():
    background_css = """
    <style>
    .stApp {
        background-color: #fff3e6 !important;
    }
    .stHeader, .stSuccess, .stError, .stButton > button {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 8px !important;
        padding: 8px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    h1, h2, h3, h4 {
        color: #d48b6b !important;
    }
    .stDivider {
        border-top: 2px solid #d48b6b !important;
    }
    /* 彻底隐藏音效播放器：不显示、不占空间、不可见 */
    .feedback-audio {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        width: 0px !important;
    }
    /* 优化按钮样式，更适合孩子点击 */
    .stButton > button {
        font-size: 16px !important;
        font-weight: 500 !important;
    }
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)

# ---------------------- 问答纯提示音功能（后台自动播放，无界面播放器） ----------------------
def generate_tone(frequency, duration=0.12, sample_rate=44100):
    """生成短信式纯提示音，轻量化无资源占用"""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    tone = 0.2 * np.sin(2 * np.pi * frequency * t)
    tone = (tone * 32767).astype(np.int16)
    audio_buffer = BytesIO()
    wavfile.write(audio_buffer, sample_rate, tone)
    audio_buffer.seek(0)
    return audio_buffer

def play_feedback_sound(is_correct):
    """答对/答错音效：后台自动播放，页面无任何播放器显示"""
    # 用with包裹，绑定隐藏样式，彻底不显示播放器
    with st.container(border=False, key="feedback_container"):
        st.markdown('<div class="feedback-audio">', unsafe_allow_html=True)
        if is_correct:
            # 答对：清脆单音阶（更简洁，无多余播放器），也可保留双音阶（同样不显示）
            tone_success = generate_tone(880, duration=0.2)
            st.audio(tone_success, format='audio/wav', autoplay=True)
        else:
            # 答错：低沉单音阶，自动播放
            tone_error = generate_tone(220, duration=0.2)
            st.audio(tone_error, format='audio/wav', autoplay=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- 页面基础配置 + 音频URL变量 ----------------------
st.set_page_config(
    page_title="Chloe's 双语阅读小屋 | Anne of Green Gables",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 音频URL存入变量
ENGLISH_AUDIO_URL = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/english_anne.mp3"
CHINESE_AUDIO_URL = "https://raw.githubusercontent.com/eachguo/chloe-reading-game/main/Audio/chinese_anne.mp3"

# 应用背景样式（含隐藏播放器样式）
set_macaron_warm_background()

# ---------------------- 页面标题 ----------------------
st.title("Chloe's 双语阅读小屋 📚")
st.subheader("《安妮的绿山墙》| Anne of Green Gables")
st.divider()

# ---------------------- 趣味段落阅读（播放条永久可见） ----------------------
st.header("趣味段落阅读 | Fun Paragraph Reading")
# 英文原文+永久播放条
st.subheader("📖 英文原文 | English Original")
english_paragraph = """Anne Shirley was not what the Cuthberts had expected. They had sent for a boy to help them with the farm work, but instead, a thin, red-haired girl with big eyes stood before them. She talked and talked, telling them about her life in the orphanage and her dreams of having a real home. Anne loved to imagine things—she called the cherry tree outside her window a "snow queen" and the brook a "silver thread". For her, the world was full of magic and beauty, even when life was hard. She hoped that the Cuthberts would keep her and that she would finally have a place to call home."""
st.write(english_paragraph)
st.audio(ENGLISH_AUDIO_URL, format="audio/mp3")
st.caption("英文语音朗读 | English Audio")

st.divider()

# 中文翻译+永久播放条
st.subheader("📖 中文翻译 | Chinese Translation")
chinese_paragraph = """安妮·雪莉并不是卡斯伯特兄妹所期待的那样。他们本来申请了一个男孩来帮忙打理农场的活计，可站在他们面前的，却是一个瘦小、红头发、有着一双大眼睛的女孩。她滔滔不绝地说着，跟他们讲述自己在孤儿院的生活，以及拥有一个真正家的梦想。安妮喜欢幻想——她把窗外的樱桃树称作“白雪女王”，把小溪称作“银线”。对她来说，即便生活艰难，这个世界也依然充满了魔法与美好。她希望卡斯伯特兄妹能留下她，希望自己终于能有一个可以称之为“家”的地方。"""
st.write(chinese_paragraph)
st.audio(CHINESE_AUDIO_URL, format="audio/mp3")
st.caption("中文语音朗读 | Chinese Audio")

st.divider()

# ---------------------- 互动思考选择题（零延迟、自动发声、无多余播放器） ----------------------
st.header("互动思考小问答 🧠")
st.success("💡 点击你认为正确的选项，自动播放提示音哦！")

# 问题列表
questions_list = [
    (
        "1. 卡斯伯特兄妹一开始想要什么？| What did the Cuthberts want at first?",
        ["A. 一个女孩 | A girl", "B. 一个男孩 | A boy", "C. 一只小狗 | A dog", "D. 一只小猫 | A cat"],
        1
    ),
    (
        "2. 安妮的头发是什么颜色的？| What color is Anne's hair?",
        ["A. 黑色 | Black", "B. 棕色 | Brown", "C. 红色 | Red", "D. 金色 | Blonde"],
        2
    ),
    (
        "3. 安妮把樱桃树称作什么？| What did Anne call the cherry tree?",
        ["A. 白雪女王 | Snow Queen", "B. 银线 | Silver Thread", "C. 魔法树 | Magic Tree", "D. 家园树 | Home Tree"],
        0
    ),
    (
        "4. 安妮的梦想是什么？| What was Anne's dream?",
        ["A. 环游世界 | Travel around the world", "B. 拥有真正的家 | Have a real home", "C. 成为老师 | Be a teacher", "D. 成为医生 | Be a doctor"],
        1
    )
]

# 遍历展示问题
for q_idx, (question, options, correct_idx) in enumerate(questions_list):
    st.subheader(question)
    col1, col2, col3, col4 = st.columns(4)
    col_list = [col1, col2, col3, col4]
    
    for i, option in enumerate(options):
        with col_list[i]:
            # 全局唯一key，避免重复报错
            btn_key = f"q_{q_idx}_opt_{i}_{hash(question + option)}"
            if st.button(option, key=btn_key, use_container_width=True):
                # 先视觉反馈，再自动播放提示音（无播放器显示）
                if i == correct_idx:
                    st.success("🎉 答对啦！太棒了！ | Correct! You're amazing!")
                else:
                    st.error("❌ 再试试哦！ | Oops, try again!")
                play_feedback_sound(is_correct=(i == correct_idx))
    st.divider()

# ---------------------- 底部结束语 ----------------------
st.write("### 🌟 下次我们一起阅读更多有趣的故事吧！ | Let's read more interesting stories next time!")