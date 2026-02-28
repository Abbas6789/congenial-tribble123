import streamlit as st
import pandas as pd
import os
import base64
import json
import plotly.graph_objects as go
import time
from datetime import datetime

# --- بنیادی سیٹنگز ---
st.set_page_config(page_title="Abbas Ultimate Bot", layout="wide")
DB_FILE = "master_database.csv"
K = "x7k9p2m4q8r1t5v3n6z0y"

# --- ڈیٹا ہینڈلنگ (ڈی کوڈنگ) ---
def decrypt(en):
    try:
        b = base64.b64decode(en)
        d = bytes(x ^ ord(K[i % len(K)]) for i, x in enumerate(b))
        return json.loads(d.decode())
    except: return None

# --- ڈیٹا سیو کرنا ---
if 'd' in st.query_params:
    sd = decrypt(st.query_params['d'])
    if sd:
        row = {"Time": datetime.now().strftime("%H:%M:%S"), "Game": sd['g']['h'], "Multiplier": float(sd['i']['v'])}
        df_new = pd.DataFrame([row])
        if not os.path.isfile(DB_FILE): df_new.to_csv(DB_FILE, index=False)
        else: df_new.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- مین ڈیش بورڈ UI ---
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🚀 ABBAS MASTER PREDICTOR</h1>", unsafe_allow_key=True)

if os.path.isfile(DB_FILE):
    df = pd.read_csv(DB_FILE)
    game_list = df['Game'].unique()
    selected_game = st.sidebar.selectbox("Select Your Game", game_list)
    g_data = df[df['Game'] == selected_game]
    last_val = g_data['Multiplier'].iloc[-1]

    # 1. ✈️ حرکت کرتا ہوا جہاز اور لائیو X (Visual Tool)
    st.markdown(f"""
        <div style="text-align: center; background: #0e1117; padding: 40px; border-radius: 20px; border: 3px solid #00ffcc; margin-bottom: 20px;">
            <div style="font-size: 80px; font-weight: bold; color: white; text-shadow: 2px 2px #00ffcc;">{last_val}x</div>
            <div style="font-size: 60px; animation: flyPlane 2s infinite alternate;">✈️</div>
            <p style="color: #888;">جہاز اڑ رہا ہے یا کریش ہو گیا...</p>
            <style>
                @keyframes flyPlane {{
                    0% {{ transform: translateY(0px) translateX(-10px); }}
                    100% {{ transform: translateY(-30px) translateX(10px); }}
                }}
            </style>
        </div>
    """, unsafe_allow_key=True)

    # 2. 🚨 بٹن سسٹم (Manual Prediction)
    st.write("---")
    if st.button('🎯 GET NEXT PREDICTION (اگلا سگنل چیک کریں)', use_container_width=True):
        with st.spinner('پچھلی ہسٹری کا تجزیہ ہو رہا ہے...'):
            time.sleep(0.5) # تھوڑی سی تاخیر تاکہ سپیڈ محسوس ہو
            avg_val = g_data['Multiplier'].tail(12).mean()
            
            # سمارٹ لاجک (Prediction Logic)
            if avg_val < 1.7:
                msg, color, target = "🟢 BET NOW (High Chance)", "#00ffcc", round(avg_val * 1.4, 2)
            elif last_val > 6:
                msg, color, target = "🔴 DANGER: WAIT (Cool Down)", "#ff4b4b", "Skip Now"
            else:
                msg, color, target = "🟡 SAFE BET (Medium)", "#ffff00", 1.65

            st.markdown(f"""
                <div style="background:{color}; padding:30px; border-radius:15px; text-align:center; color:black;">
                    <h1 style="margin:0;">{msg}</h1>
                    <h2 style="margin:0;">Expected Target: {target}x</h2>
                </div>
            """, unsafe_allow_key=True)
    st.write("---")

    # 3. پروفیشنل گراف اور میٹر
    col1, col2 = st.columns(2)
    with col1:
        # رسک میٹر
        risk_val = 100 if g_data['Multiplier'].tail(5).mean() < 1.6 else 30
        fig = go.Figure(go.Indicator(
            mode = "gauge+number", value = risk_val,
            title = {'text': "Winning Chance %"},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#00ffcc"},
                     'steps': [{'range': [0, 40], 'color': "red"}, {'range': [70, 100], 'color': "green"}]}
        ))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # ہسٹری چارٹ
        st.subheader("📊 Last 20 Rounds History")
        st.line_chart(g_data['Multiplier'].tail(20))

else:
    st.info("سسٹم ریڈی ہے! جیسے ہی آپ گیم شروع کریں گے، ڈیٹا یہاں خود بخود نظر آنا شروع ہو جائے گا۔")
    
