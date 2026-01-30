# 导入必备库
import streamlit as st
from gtts import gTTS
from io import BytesIO
import numpy as np
from scipy.io import wavfile

# ---------------------- 马卡龙纯色背景（修复：只隐藏问答反馈的音频，保留段落朗读播放器） ----------------------
def set_macaron_warm_background():
    """纯马卡龙浅蜜桃色背景，柔和不刺眼，适配儿童视觉"""
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
    /* 只隐藏问答反馈的音频（通过自定义类，不影响段落朗读） */
    .feedback-audio {
        display: none !important;
    }
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)

# ---------------------- 语音朗读 + 纯提示音功能（核心修复：优化性能+分离音频显示） ----------------------
def text_to_speech(text, lang):
    """中英文文本转语音，优化性能，避免阻塞"""
    try:
        # 优化：减少音频生成的资源占用，快速返回缓冲区
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        st.warning(f"⚠️ 语音生成失败：{str(e)} | Speech generation failed: {str(e)}")
        return None

def generate_tone(frequency, duration=0.2, sample_rate=44100):
    """生成纯音频提示音（无人类语言，类似手机短信提示音），优化生成速度"""
    # 生成时间轴（简化计算，提升速度）
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # 生成正弦波音频（控制音量避免刺耳，减少数据量）
    tone = 0.2 * np.sin(2 * np.pi * frequency * t)  # 降低音量，减少计算压力
    # 转换为16位整型音频格式（符合wav标准，快速写入）
    tone = (tone * 32767).astype(np.int16)
    # 写入字节流缓冲区
    audio_buffer = BytesIO()
    wavfile.write(audio_buffer, sample_rate, tone)
    audio_buffer.seek(0)
    return audio_buffer

def play_feedback_sound(is_correct):
    """播放纯音频反馈（只隐藏该音频播放器，不影响段落朗读，优化响应速度）"""
    # 给问答反馈音频添加自定义类，实现隐藏且不阻塞
    if is_correct:
        # 答对提示音：清脆双音阶「叮咚」（高频，区分度高，缩短时长提升速度）
        tone_high1 = generate_tone(880, duration=0.12)  # 缩短时长，减少延迟
        tone_high2 = generate_tone(1320, duration=0.12)
        # 添加自定义类隐藏播放器，autoplay=True且不阻塞
        st.markdown('<div class="feedback-audio">', unsafe_allow_html=True)
        st.audio(tone_high1, format='audio/wav', autoplay=True)
        st.audio(tone_high2, format='audio/wav', autoplay=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # 答错提示音：低沉单音阶「啊欧」（低频，柔和不打击信心）
        tone_low = generate_tone(220, duration=0.25)  # 缩短时长，减少延迟
        st.markdown('<div class="feedback-audio">', unsafe_allow_html=True)
        st.audio(tone_low, format='audio/wav', autoplay=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- 页面基础配置 ----------------------
st.set_page_config(
    page_title="Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut",
    page_icon="📚",
    layout="centered"
)

# 应用背景样式
set_macaron_warm_background()

# ---------------------- 核心内容（修复：段落语音正常播放，消除问答延迟） ----------------------
st.title("Chloe's 双语阅读小屋 | Chloe's Bilingual Reading Hut")
story_topic_cn = "《安妮的绿山墙》"
story_topic_en = "Anne of Green Gables"
st.subheader(f"—— {story_topic_cn} 专属阅读版 | Exclusive Reading Edition of {story_topic_en}")
st.divider()

# 语音朗读开关（优化：提前初始化，避免开关状态切换导致资源重复加载）
audio_toggle = st.toggle("开启/关闭语音朗读 | Enable/Disable Text-to-Speech", value=False)
st.caption("提示：开启后，展开阅读内容即可播放语音 | Tip: After enabling, expand the reading content to play audio.")
st.divider()

# 中英双语阅读 + 语音朗读（修复：播放器正常显示，语音可播放）
st.header("趣味段落阅读 | Fun Paragraph Reading")

# 英文原文
with st.expander("点击展开「英文原文」 | Click to Expand [English Original]", expanded=True):
    english_paragraph = """Anne Shirley was not what the Cuthberts had expected. They had sent for a boy to help them with the farm work, but instead, a thin, red-haired girl with big eyes stood before them. She talked and talked, telling them about her life in the orphanage and her dreams of having a real home. Anne loved to imagine things—she called the cherry tree outside her window a "snow queen" and the brook a "silver thread". For her, the world was full of magic and beauty, even when life was hard. She hoped that the Cuthberts would keep her and that she would finally have a place to call home."""
    st.write(english_paragraph)
    
    if audio_toggle:
        st.subheader("英文语音朗读 | English Audio Reading")
        # 优化：提前生成音频，避免点击展开时阻塞
        english_audio = text_to_speech(english_paragraph, lang='en')
        if english_audio:
            # 正常显示播放器，允许播放/暂停
            st.audio(english_audio, format='audio/mp3')

# 中文翻译
with st.expander("点击展开「中文翻译」 | Click to Expand [Chinese Translation]", expanded=True):
    chinese_paragraph = """安妮·雪莉并不是卡斯伯特兄妹所期待的那样。他们本来申请了一个男孩来帮忙打理农场的活计，可站在他们面前的，却是一个瘦小、红头发、有着一双大眼睛的女孩。她滔滔不绝地说着，跟他们讲述自己在孤儿院的生活，以及拥有一个真正家的梦想。安妮喜欢幻想——她把窗外的樱桃树称作“白雪女王”，把小溪称作“银线”。对她来说，即便生活艰难，这个世界也依然充满了魔法与美好。她希望卡斯伯特兄妹能留下她，希望自己终于能有一个可以称之为“家”的地方。"""
    st.write(chinese_paragraph)
    
    if audio_toggle:
        st.subheader("中文语音朗读 | Chinese Audio Reading")
        # 优化：提前生成音频，避免点击展开时阻塞
        chinese_audio = text_to_speech(chinese_paragraph, lang='zh-CN')
        if chinese_audio:
            # 正常显示播放器，允许播放/暂停
            st.audio(chinese_audio, format='audio/mp3')

st.divider()

# ---------------------- 互动思考选择题（修复：消除延迟，响应流畅） ----------------------
st.header("互动思考问题 | Interactive Thinking Questions")
st.success("点击你认为正确的选项，答对会有清脆提示音哦！ | Click the option you think is correct, you'll hear a crisp prompt if you're right!")

# 定义问题和选项（格式：(问题, 选项列表, 正确答案索引)）
questions_list = [
    (
        "1. What did the Cuthberts want at first? （卡斯伯特兄妹一开始想要什么？）",
        ["A. A girl (一个女孩)", "B. A boy (一个男孩)", "C. A dog (一只小狗)", "D. A cat (一只小猫)"],
        1  # 正确选项：B
    ),
    (
        "2. What color is Anne's hair? （安妮的头发是什么颜色的？）",
        ["A. Black (黑色)", "B. Brown (棕色)", "C. Red (红色)", "D. Blonde (金色)"],
        2  # 正确选项：C
    ),
    (
        "3. What did Anne call the cherry tree? （安妮把樱桃树称作什么？）",
        ["A. Snow Queen (白雪女王)", "B. Silver Thread (银线)", "C. Magic Tree (魔法树)", "D. Home Tree (家园树)"],
        0  # 正确选项：A
    ),
    (
        "4. What was Anne's dream? （安妮的梦想是什么？）",
        ["A. To travel around the world (环游世界)", "B. To have a real home (拥有一个真正的家)", "C. To be a teacher (成为一名老师)", "D. To be a doctor (成为一名医生)"],
        1  # 正确选项：B
    )
]

# 遍历展示每个问题，实现横向按钮+流畅反馈
for question, options, correct_idx in questions_list:
    st.subheader(question)
    # 4列布局，横向排列选项按钮
    col1, col2, col3, col4 = st.columns(4)
    col_list = [col1, col2, col3, col4]
    
    # 为每个选项创建独立按钮（优化：唯一key，避免冲突，提升响应速度）
    for i, option in enumerate(options):
        with col_list[i]:
            btn_key = f"q_{hash(question)}_{i}"  # 更稳定的唯一key
            if st.button(option, key=btn_key):
                # 优化：先反馈视觉提示，再播放音效，减少延迟感知
                if i == correct_idx:
                    st.success("🎉 答对啦！太棒了！ | Correct! You're amazing!")
                else:
                    st.error("❌ 再试试哦！ | Oops, try again!")
                # 播放音效（异步感知，不阻塞视觉反馈）
                play_feedback_sound(is_correct=(i == correct_idx))
    st.divider()

# ---------------------- 底部结束语 ----------------------
st.write("### 下次我们一起阅读更多有趣的故事吧！ | Let's read more interesting stories next time!")