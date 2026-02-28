import streamlit as st
import base64
import json
import pandas as pd
import os
from datetime import datetime

# --- ⚙️ سیٹنگز ---
st.set_page_config(page_title="Abbas 47-in-1 Master Bot", layout="wide")
K = "x7k9p2m4q8r1t5v3n6z0y"
DB_FILE = "master_database.csv"

# --- 🔐 ڈی کوڈنگ ---
def decrypt(en):
    try:
        b = base64.b64decode(en)
        d = bytes(x ^ ord(K[i % len(K)]) for i, x in enumerate(b))
        return json.loads(d.decode())
    except: return None

# --- 📁 آٹو سیونگ (ان لمیٹڈ) ---
def save(data):
    row = {"TS": datetime.now(), "G": data['g']['h'], "V": float(data['i']['v'])}
    df = pd.DataFrame([row])
    if not os.path.isfile(DB_FILE): df.to_csv(DB_FILE, index=False)
    else: df.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- 🛰️ ڈیٹا وصول کرنا ---
if 'd' in st.query_params:
    sd = decrypt(st.query_params['d'])
    if sd: save(sd)

# --- 📊 ڈیش بورڈ ---
st.title("🎮 47-in-1 Universal Signal Bot")

if os.path.isfile(DB_FILE):
    full_df = pd.read_csv(DB_FILE)
    st.sidebar.metric("Total Rounds", len(full_df))
    
    # گیم سلیکٹر (خود بخود تمام 47 گیمز یہاں آ جائیں گی)
    game = st.sidebar.selectbox("Select Your Game", full_df['G'].unique())
    g_data = full_df[full_df['G'] == game].tail(100)

    # 🎯 سگنل بٹن (یہ اب ہمیشہ یہاں رہے گا)
    if st.button("🚀 GET SIGNAL (Analysis)"):
        if len(g_data) < 10:
            st.warning("کم از کم 10 راؤنڈز کا ڈیٹا جمع ہونے دیں...")
        else:
            avg = g_data['V'].tail(5).mean()
            if avg < 1.8: res, col = "SAFE BET (1.50x) ✅", "green"
            elif avg > 4.0: res, col = "DANGER: SKIP 🔴", "red"
            else: res, col = "WAIT FOR PINK 🟡", "orange"
            st.markdown(f"<h2 style='color:{col}'>{res}</h2>", unsafe_allow_key=True)

    st.line_chart(g_data['V'])
else:
    st.info("سسٹم ریڈی ہے! کروم میں اسکرپٹ چلائیں، ڈیٹا خود بخود یہاں بھرنا شروع ہو جائے گا۔")
        
