import streamlit as st
from the_brain import ProbabilisticBrain
from scanner import find_history_endpoints

st.set_page_config(page_title="Aviator AI Tool", layout="wide")
st.title("🚀 Aviator AI Predictor")

brain = ProbabilisticBrain()

# سائیڈ بار کنٹرول
st.sidebar.header("سیٹ اپ")
game_link = st.sidebar.text_input("گیم کا یو آر ایل ڈالیں")
if st.sidebar.button("آٹو اسکین کریں"):
    result = find_history_endpoints(game_link)
    st.sidebar.write(result)

# مین اسکرین
col1, col2 = st.columns(2)

with col1:
    st.subheader("ڈیٹا انٹری")
    manual_input = st.text_area("ہسٹری یہاں ڈالیں (مثال: 1.2, 2.5, 1.1)", height=150)
    if st.button("تجزیہ شروع کریں"):
        data = [float(x.strip()) for x in manual_input.split(",") if x.strip()]
        brain.update_history(data)
        st.success("ڈیٹا اپ لوڈ ہو گیا!")

with col2:
    st.subheader("لائیو سگنل")
    prob, status = brain.calculate_logic()
    st.metric("جیتنے کا چانس", f"{prob*100}%")
    st.info(f"مشورہ: {status}")

if brain.history:
    st.line_chart(brain.history)
