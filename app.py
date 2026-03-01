import streamlit as st
import pandas as pd
import os
import base64
import json
import time
from datetime import datetime

# --- پیج سیٹنگز (موبائل ڈبل اسکرین کے لیے بہترین) ---
st.set_page_config(page_title="FINAL VIP PREDICTOR", layout="centered")

DB_FILE = "aviator_master_db.csv"
K = "x7k9p2m4q8r1t5v3n6z0y"

# --- ڈیٹا بیس فنکشن ---
def save_to_storage(val):
    current_time = datetime.now().strftime("%H:%M:%S")
    new_entry = pd.DataFrame([{"Time": current_time, "Multiplier": float(val)}])
    if not os.path.isfile(DB_FILE):
        new_entry.to_csv(DB_FILE, index=False)
    else:
        new_entry.to_csv(DB_FILE, mode='a', header=False, index=False)

def load_storage():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Time", "Multiplier"])

# --- ڈیٹا ریسیور ---
def decrypt_data(data):
    try:
        b = base64.b64decode(data.replace('-', '+').replace('_', '/'))
        out = "".join(chr(b[i] ^ ord(K[i % len(K)])) for i in range(len(b)))
        return json.loads(out)
    except: return None

# --- خوبصورت ڈیزائن (CSS) ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #00FF00; color: black; font-weight: bold; font-size: 18px; border: none; }
    .stButton>button:active { background-color: #008000; color: white; }
    .prediction-box { background: #1E1E1E; padding: 20px; border-radius: 15px; text-align: center; border: 2px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #00FF00;'>🛰️ SYSTEM ONLINE</h2>", unsafe_allow_html=True)

# آٹو ڈیٹا کیپچر
params = st.query_params
if "d" in params:
    res = decrypt_data(params["d"])
    if res:
        val = res.get('i', {}).get('v', '0')
        save_to_storage(val)
        st.query_params.clear()
        st.rerun()

df = load_storage()

# --- مین ڈیش بورڈ ---
if not df.empty:
    last_num = df.iloc[-1]['Multiplier']
    st.write(f"✅ آخری نمبر ریکارڈ ہوا: **{last_num}x**")
    
    # --- ان لمیٹڈ پش بٹن ---
    if st.button("🚀 GENERATE NEXT SIGNAL"):
        with st.spinner('ڈیٹا اسکین ہو رہا ہے...'):
            time.sleep(0.5) # سیکنڈوں میں رزلٹ
            
            # اسمارٹ پریڈکشن لاجک
            if last_num < 1.60:
                target = "1.80x - 2.40x"
                signal = "PLACE BET NOW! ✅"
                color = "#00FF00"
            elif last_num < 3.0:
                target = "1.25x - 1.50x"
                signal = "SAFE PLAY ONLY ⚠️"
                color = "#FFA500"
            else:
                target = "SKIP THIS ROUND"
                signal = "TOO RISKY! ❌"
                color = "#FF4B4B"
            
            # فائنل رزلٹ ڈسپلے
            st.markdown(f"""
            <div class="prediction-box" style="border-top: 8px solid {color};">
                <h3 style="color: white; margin-bottom: 5px;">اگلا ٹارگٹ</h3>
                <h1 style="color: {color}; font-size: 45px; margin: 0;">{target}</h1>
                <h4 style="color: {color};">{signal}</h4>
            </div>
            """, unsafe_allow_html=True)

    # گراف
    st.line_chart(df.tail(12).set_index('Time')['Multiplier'])
    
    with st.expander("📁 اسٹوریج ہسٹری"):
        st.table(df.tail(10))
        if st.button("🗑️ ڈیٹا ڈیلیٹ کریں"):
            if os.path.exists(DB_FILE): os.remove(DB_FILE)
            st.rerun()
else:
    st.info("گیم سے ڈیٹا آنے کا انتظار ہے... جیسے ہی جہاز اڑے گا، یہاں سگنل بٹن ایکٹیو ہو جائے گا۔")

st.markdown("<p style='text-align: center; font-size: 10px; color: gray;'>v4.0 Final Auto-Pilot Mode</p>", unsafe_allow_html=True)
    
