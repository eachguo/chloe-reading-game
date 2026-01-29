def set_fun_background():
    """设置马卡龙暖色系背景（浅蜜桃色+小云朵图案，低饱和度，不喧宾夺主）"""
    background_css = """
    <style>
    .stApp {
        background-color: #fff3e6;  /* 马卡龙浅蜜桃色，温暖柔和 */
        background-image: url("https://picsum.photos/id/1025/1920/1080");  /* 童趣云朵图案 */
        background-size: cover;
        background-opacity: 0.08;  /* 透明度8%，非常淡，不影响阅读 */
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    /* 优化文本区域背景，保证可读性 */
    .stExpander, .stHeader, .stSuccess {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 8px !important;
        padding: 10px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)