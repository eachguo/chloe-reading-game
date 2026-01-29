# 互动单词配对（优化版，玩法清晰）
st.header("🎮 单词配对小游戏 | Word Matching Game")
st.success("💡 游戏规则：用鼠标画线，把左边的数字和右边对应的字母连起来，提交后查看对错")

# 左右两列，明确对应关系
col1, col2 = st.columns(2)
with col1:
    st.subheader("英文单词 | English Words")
    st.write("1. orphanage")
    st.write("2. farm")
with col2:
    st.subheader("中文释义 | Chinese Meanings")
    st.write("A. 农场")
    st.write("B. 孤儿院")

# 互动画布
st.write("### 🎨 点击下方画布画线配对（例如：1 → B，2 → A）")
canvas_result = st_canvas(
    fill_color="rgba(255,255,255,0)",
    stroke_width=3,
    stroke_color="#d48b6b",
    background_color="#fdf6f0",
    height=200,
    width=600,
    drawing_mode="freedraw",
    key="canvas"
)

# 提交按钮与反馈
if st.button("✅ 提交答案并判断 | Submit Answer and Judge"):
    st.write("### ✅ 正确配对答案：")
    st.write("1. orphanage → B. 孤儿院")
    st.write("2. farm → A. 农场")
    st.write("### 🎯 请对照你的连线检查是否正确！")