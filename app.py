# 导入必备库
import streamlit as st
from gtts import gTTS
from io import BytesIO

# ---------------------- 马卡龙纯色背景 ----------------------
def set_macaron_warm_background():
    background_css = """
    <style>
    .stApp {
        background-color: #fff3e6 !important;
    }
    .stExpander, .stHeader, .stSuccess, .stButton > button, .stTextInput > div > div, .stToggle > div {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 8px !important;
        padding: 10px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    h1, h2, h3, h4 {
        color: #d48b6b !important;
    }
    .stDivider {
        border-top: 2px solid #d48b6b !important;
    }
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)

# ---------------------- 语音朗读 + 答题音效功能 ----------------------
def text_to_speech(text, lang):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        st.warning(f"⚠️ 语音生成失败：{str(e)} | Speech generation failed: {str(e)}")
        return None

def play_sound(sound_type):
    # 直接生成不同的音效反馈
    audio_buffer = BytesIO()
    if sound_type == "correct":
        # 答对音效：叮咚
        tts = gTTS(text="叮咚", lang='zh-CN', slow=False)
    else:
        # 答错音效：啊欧
        tts = gTTS(text="啊欧", lang='zh-CN', slow=False)
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    st.audio(audio_buffer, format='audio/mp3', autoplay=True)

# ---------------------- 页面基础配置 ----------------------
st.set_page_config(
    page_title="Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut",
    page_icon="📚",
    layout="centered"
)

set_macaron_warm_background()

# ---------------------- 核心内容 ----------------------
st.title("Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut")
story_topic_cn = "《安妮的绿山墙》"
story_topic_en = "Anne of Green Gables"
st.subheader(f"—— {story_topic_cn} 专属阅读版 | Exclusive Reading Edition of {story_topic_en}")
st.divider()

# 语音朗读开关
audio_toggle = st.toggle("开启/关闭语音朗读 | Enable/Disable Text-to-Speech", value=False)
st.caption("提示：开启后，展开阅读内容即可播放语音 | Tip: After enabling, expand the reading content to play audio.")
st.divider()

# 中英双语阅读 + 语音朗读
st.header("趣味段落阅读 | Fun Paragraph Reading")

# 英文原文
with st.expander("点击展开「英文原文」 | Click to Expand [English Original]", expanded=True):
    english_paragraph = """Anne Shirley was not what the Cuthberts had expected. They had sent for a boy to help them with the farm work, but instead, a thin, red-haired girl with big eyes stood before them. She talked and talked, telling them about her life in the orphanage and her dreams of having a real home. Anne loved to imagine things—she called the cherry tree outside her window a "snow queen" and the brook a "silver thread". For her, the world was full of magic and beauty, even when life was hard. She hoped that the Cuthberts would keep her and that she would finally have a place to call home."""
    st.write(english_paragraph)
    
    if audio_toggle:
        st.subheader("英文语音朗读 | English Audio Reading")
        english_audio = text_to_speech(english_paragraph, lang='en')
        if english_audio:
            st.audio(english_audio, format='audio/mp3')

# 中文翻译
with st.expander("点击展开「中文翻译」 | Click to Expand [Chinese Translation]", expanded=True):
    chinese_paragraph = """安妮·雪莉并不是卡斯伯特兄妹所期待的那样。他们本来申请了一个男孩来帮忙打理农场的活计，可站在他们面前的，却是一个瘦小、红头发、有着一双大眼睛的女孩。她滔滔不绝地说着，跟他们讲述自己在孤儿院的生活，以及拥有一个真正家的梦想。安妮喜欢幻想——她把窗外的樱桃树称作“白雪女王”，把小溪称作“银线”。对她来说，即便生活艰难，这个世界也依然充满了魔法与美好。她希望卡斯伯特兄妹能留下她，希望自己终于能有一个可以称之为“家”的地方。"""
    st.write(chinese_paragraph)
    
    if audio_toggle:
        st.subheader("中文语音朗读 | Chinese Audio Reading")
        chinese_audio = text_to_speech(chinese_paragraph, lang='zh-CN')
        if chinese_audio:
            st.audio(chinese_audio, format='audio/mp3')

st.divider()

# ---------------------- 互动思考选择题（点击选项直接反馈） ----------------------
st.header("互动思考问题 | Interactive Thinking Questions")
st.success("点击你认为正确的选项，答对会有叮咚声哦！ | Click the option you think is correct, you'll hear a 'ding-dong' if you're right!")

# 定义问题和选项
questions_list = [
    (
        "1. What did the Cuthberts want at first? （卡斯伯特兄妹一开始想要什么？）",
        ["A. A girl (一个女孩)", "B. A boy (一个男孩)", "C. A dog (一只小狗)", "D. A cat (一只小猫)"],
        1  # 正确选项是B
    ),
    (
        "2. What color is Anne's hair? （安妮的头发是什么颜色的？）",
        ["A. Black (黑色)", "B. Brown (棕色)", "C. Red (红色)", "D. Blonde (金色)"],
        2  # 正确选项是C
    ),
    (
        "3. What did Anne call the cherry tree? （安妮把樱桃树称作什么？）",
        ["A. Snow Queen (白雪女王)", "B. Silver Thread (银线)", "C. Magic Tree (魔法树)", "D. Home Tree (家园树)"],
        0  # 正确选项是A
    ),
    (
        "4. What was Anne's dream? （安妮的梦想是什么？）",
        ["A. To travel around the world (环游世界)", "B. To have a real home (拥有一个真正的家)", "C. To be a teacher (成为一名老师)", "D. To be a doctor (成为一名医生)"],
        1  # 正确选项是B
    )
]

# 遍历展示每个问题
for question, options, correct_idx in questions_list:
    st.subheader(question)
    col1, col2, col3, col4 = st.columns(4)
    # 每个选项做成一个按钮
    for i, option in enumerate(options):
        with [col1, col2, col3, col4][i]:
            if st.button(option, key=f"{question}_{i}"):
                if i == correct_idx:
                    st.success("🎉 答对啦！太棒了！ | Correct! You're amazing!")
                    play_sound("correct")
                else:
                    st.error("❌ 啊欧，再试试！ | Oops, try again!")
                    play_sound("wrong")
    st.divider()

# ---------------------- 底部结束语 ----------------------
st.write("### 下次我们一起阅读更多有趣的故事吧！ | Let's read more interesting stories next time!")