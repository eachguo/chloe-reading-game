def set_macaron_warm_background():
    """稳定兼容版：马卡龙浅蜜桃色 + 生肖图案（若隐若现）"""
    background_css = """
    <style>
    /* 马卡龙浅蜜桃色底色 */
    .stApp {
        background-color: #fff3e6;
    }
    /* 生肖图案若隐若现 */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("https://picsum.photos/id/1076/1920/1080");
        background-size: 200px 200px;
        background-repeat: repeat;
        opacity: 0.03;
        z-index: -1;
        pointer-events: none;
    }
    /* 文本区域加固，保证清晰 */
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