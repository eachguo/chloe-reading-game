# --- 修改后的播放逻辑 (替换 app.py 中对应部分) ---

# 1. 首先定义本地可能存在的音频路径
local_path_cn = f"audio/{selected_title}_CN.mp3"
local_path_en = f"audio/{selected_title}_EN.mp3"

# 2. 在“故事内容”下方增加大宝专用的播放区域
st.write("---")
st.write("🔊 **听听故事吧 | Listen to the Story**")

# 检查是否有云端链接 (表格里的)
audio_link = str(row.get('audio_url', '')).strip()

if "http" in audio_link and not audio_link.startswith('nan'):
    # 优先播放您在表格里填写的正式链接
    st.audio(audio_link)
elif os.path.exists(local_path_cn) or os.path.exists(local_path_en):
    # 如果表格里没填链接，但本地工场已经生成了文件，就直接给大宝播本地的
    col_audio1, col_audio2 = st.columns(2)
    if os.path.exists(local_path_cn):
        with col_audio1:
            st.caption("🇨🇳 中文朗读")
            st.audio(local_path_cn)
    if os.path.exists(local_path_en):
        with col_audio2:
            st.caption("🇬🇧 英文朗读")
            st.audio(local_path_en)
else:
    st.info("✨ 姥爷正在录制中，稍后再来听哦！ | Audio coming soon!")