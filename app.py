def set_macaron_warm_background():
    """极简版马卡龙暖色系背景（浅蜜桃色，无额外图片，保证不报错）"""
    background_css = """
    <style>
    .stApp {
        background-color: #fff3e6;  /* 纯马卡龙浅蜜桃色，无图片，绝对不报错 */
    }
    .stExpander, .stHeader, .stSuccess, .stButton > button {
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