# --------------------------
# 预加载音频（和《安妮的绿山墙》一致，解决浏览器拦截问题）
# --------------------------
# 隐藏的预加载播放器，让浏览器提前缓存音频
st.audio(correct_audio_url, format="audio/mp3", loop=False, autoplay=False, key="preload_correct")
st.audio(wrong_audio_url, format="audio/mp3", loop=False, autoplay=False, key="preload_wrong")

# 用CSS隐藏这个预加载播放器
st.markdown("""
    <style>
        [data-testid="stAudio"][key="preload_correct"],
        [data-testid="stAudio"][key="preload_wrong"] {
            display: none !important;
            height: 0;
            width: 0;
        }
    </style>
""", unsafe_allow_html=True)