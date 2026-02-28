import streamlit as st
from the_brain import analyze_data
from scanner import scan_site
from PIL import Image

# پیج کی بنیادی سیٹنگز
st.set_page_config(page_title="Aviator Pro Predictor", layout="centered")

st.title("🚀 Aviator Universal Predictor")
st.write("اپنا پسندیدہ طریقہ منتخب کریں اور ڈیٹا فراہم کریں:")

# مینیو یا ریڈیو بٹن بنانا
option = st.radio(
    "تجزیہ کرنے کا طریقہ منتخب کریں:",
    ("Link Scanner", "Screenshot Upload", "Manual Entry")
)

st.markdown("---")

# --- آپشن 1: لنک اسکینر (Link Scanner) ---
if option == "Link Scanner":
    st.header("🔍 Auto Web Scanner")
    url = st.text_input("گیم کا لنک (URL) یہاں پیسٹ کریں:")
    if st.button("Start Scan"):
        if url:
            with st.spinner('ویب سائٹ اسکین کی جا رہی ہے...'):
                # یہ اسکینر فائل سے نتیجہ لائے گا
                res = scan_site(url)
                st.info(f"Scanner Result: {res}")
        else:
            st.warning("براہ کرم پہلے لنک درج کریں۔")

# --- آپشن 2: اسکرین شاٹ اپ لوڈر (Screenshot Upload) ---
elif option == "Screenshot Upload":
    st.header("📸 Screenshot Analysis")
    uploaded_file = st.file_uploader("گیم ہسٹری کا تازہ ترین اسکرین شاٹ اپ لوڈ کریں", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="آپ کا اپ لوڈ کردہ اسکرین شاٹ", use_column_width=True)
        
        if st.button("Extract & Predict"):
            with st.spinner('تصویر سے نمبر نکالے جا رہے ہیں...'):
                # فی الحال یہ میسج دکھائے گا جب تک OCR مکمل سیٹ نہ ہو
                st.info("تصویر سے ڈیٹا نکالنے کا فیچر ایکٹیویٹ ہو رہا ہے...")
                st.warning("نوٹ: اگر خودکار طریقے سے نمبر نہ نکلیں تو 'Manual Entry' استعمال کریں۔")

# --- آپشن 3: مینول ڈیٹا انٹری (Manual Entry) ---
elif option == "Manual Entry":
    st.header("📊 Manual Data Entry")
    numbers_input = st.text_input("پچھلے 5 راؤنڈز کے نمبر لکھیں (مثال: 1.20, 3.50, 1.05):")
    
    if st.button("Analyze Now"):
        if numbers_input:
            try:
                # ٹیکسٹ کو نمبرز کی لسٹ میں بدلنا
                data_list = [float(x.strip()) for x in numbers_input.split(",")]
                
                with st.spinner('AI تجزیہ کر رہا ہے...'):
                    # یہ 'the_brain.py' سے حساب منگوائے گا
                    prediction = analyze_data(data_list)
                    
                    # نتیجہ دکھانا
                    st.success(f"### 🎯 Prediction: {prediction['status']}")
                    st.metric("Winning Chance", f"{prediction['percentage']}%")
            except ValueError:
                st.error("براہ کرم نمبر صحیح طرح لکھیں اور درمیان میں کوما (,) لگائیں۔")
        else:
            st.warning("تجزیہ کے لیے کچھ نمبرز لکھنا ضروری ہے۔")

st.markdown("---")
st.caption("Developed by Abbas | Powered by AI Predictor Engine")
