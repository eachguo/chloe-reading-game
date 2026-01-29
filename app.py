def set_macaron_warm_background():
    """设置马卡龙暖色系背景（浅蜜桃色+生肖图案，若隐若现）"""
    background_css = """
    <style>
    /* 整体背景：马卡龙浅蜜桃色 + 生肖图案 */
    .stApp {
        background-color: #fff3e6;  /* 马卡龙浅蜜桃底色 */
        background-image: url("https://picsum.photos/id/1076/1920/1080"), url("https://example.com/your-zodiac-pattern.png");
        background-size: cover, 200px 200px;  /* 背景图铺满，生肖图案缩小为200x200 */
        background-opacity: 0.06, 0.03;  /* 背景图6%透明度，生肖图案3%透明度 */
        background-repeat: no-repeat, repeat;  /* 背景图不重复，生肖图案平铺 */
        background-attachment: fixed, fixed;
    }
    /* 文本区域优化：保证清晰 */
    .stExpander, .stHeader, .stSuccess, .stButton > button {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 8px !important;
        padding: 10px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    /* 标题颜色统一为马卡龙暖橘色 */
    h1, h2, h3, h4 {
        color: #d48b6b !important;
    }
    /* 分割线颜色统一为马卡龙暖橘色 */
    .stDivider {
        border-top: 2px solid #d48b6b !important;
    }
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)