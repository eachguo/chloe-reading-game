# --- 5. 播放逻辑 (优化后的正式双语版) ---
    st.write("---")
    
    # 检查云端链接 (表格中)
    audio_link = str(row.get('audio_url', '')).strip()
    
    # 逻辑 A：如果表格里有正式链接
    if "http" in audio_link and not audio_link.startswith('nan'):
        st.write("🔊 **听听故事吧 | Listen to the Story**")
        st.audio(audio_link)
    
    # 逻辑 B：如果云端没链接，但本地工场已生成文件 (解决您之前的疑问)
    elif os.path.exists(local_cn) or os.path.exists(local_en):
        st.write("🔊 **语音内容已就绪 | Audio Content Ready**")
        col_left, col_right = st.columns(2)
        if os.path.exists(local_cn):
            with col_left:
                st.write("🇨🇳 **中文朗读 | Chinese**")
                st.audio(local_cn)
        if os.path.exists(local_en):
            with col_right:
                st.write("🇬🇧 **英文朗读 | English**")
                st.audio(local_en)
    
    # 逻辑 C：什么都没有时
    else:
        st.info("✨ 制作中，请稍后再来听哦！ | Audio is being prepared!")