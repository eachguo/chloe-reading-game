# --- 播放逻辑 (优化后的双语正式版) ---
    st.write("---")
    audio_link = str(row.get('audio_url', '')).strip()
    
    # 逻辑 1：如果表格里已经填了云端链接
    if "http" in audio_link and not audio_link.startswith('nan'):
        st.write("🔊 **听听故事吧 | Listen to the Story**")
        st.audio(audio_link)
    
    # 逻辑 2：如果云端没链接，但本地工场刚刚生成了文件
    elif os.path.exists(local_cn) or os.path.exists(local_en):
        st.write("🔊 **语音内容已就绪 | Audio Content Ready**")
        col_a, col_b = st.columns(2)
        if os.path.exists(local_cn):
            with col_a:
                st.write("🇨🇳 **中文朗读 | Chinese**")
                st.audio(local_cn)
        if os.path.exists(local_en):
            with col_b:
                st.write("🇬🇧 **英文朗读 | English**")
                st.audio(local_en)
    
    # 逻辑 3：什么都没有的时候
    else:
        st.info("✨ 朗读正在制作中，稍后再来听哦！ | Audio is being prepared, check back later!")