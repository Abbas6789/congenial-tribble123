import streamlit as st
import pandas as pd
import os
import base64
import json
import plotly.graph_objects as go
from datetime import datetime
import urllib.parse

# --- بنیادی سیٹنگز ---
st.set_page_config(page_title="Abbas Master Bot", layout="wide")
DB_FILE = "master_database.csv"
K = "x7k9p2m4q8r1t5v3n6z0y"

# --- ڈیٹا ڈی کوڈ کرنے کا فنکشن ---
def decrypt(en_str):
    try:
        # نشانات کو صاف کرنا
        en_str = urllib.parse.unquote(en_str).replace('-', '+').replace('_', '/')
        # پیڈنگ مکمل کرنا
        missing_padding = len(en_str) % 4
        if missing_padding:
            en_str += '=' * (4 - missing_padding)
        b = base64.b64decode(en_str)
        # XOR ڈی کوڈنگ
        decrypted_bytes = bytearray()
        for i in range(len(b)):
            decrypted_bytes.append(b[i] ^ ord(K[i % len(K)]))
        return json.loads(decrypted_bytes.decode('utf-8'))
    except:
        return None

# --- ڈیٹا وصول کرنا ---
params = st.query_params
if 'd' in params:
    sd = decrypt(params['d'])
    if sd:
        current_time = datetime.now().strftime("%H:%M:%S")
        game_name = sd.get('g', {}).get('h', 'Game_Live')
        val = sd.get('i', {}).get('v', '0')
        try:
            multiplier = float(val)
            df_new = pd.DataFrame([{"Time": current_time, "Game": game_name, "Multiplier": multiplier}])
            if not os.path.isfile(DB_FILE):
                df_new.to_csv(DB_FILE, index=False)
            else:
                df_new.to_csv(DB_FILE, mode='a', header=False, index=False)
            st.rerun()
        except:
            pass

# --- ڈیش بورڈ ڈیزائن ---
st.title("💎 ABBAS MASTER PREDICTOR")

if os.path.isfile(DB_FILE):
    df = pd.read_csv(DB_FILE).tail(50)
    game_list = df['Game'].unique()
    selected_game = st.sidebar.selectbox("Select Game", game_list)
    g_data = df[df['Game'] == selected_game]
    
    if not g_data.empty:
        last_val = g_data['Multiplier'].iloc[-1]
        st.markdown(f"""
            <div style="background: #111; padding: 20px; border-radius: 15px; border: 2px solid #00ffcc; text-align: center;">
                <h1 style="color: #00ffcc; font-size: 70px; margin: 0;">{last_val}x</h1>
                <div style="font-size: 40px; animation: move 1s infinite alternate;">✈️</div>
            </div>
            <style> @keyframes move {{ from {{transform: translateY(0px);}} to {{transform: translateY(-10px);}} }} </style>
        """, unsafe_allow_key=True)

        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button('🚀 GET NEXT SIGNAL'):
                avg = g_data['Multiplier'].tail(5).mean()
                st.success(f"اگلا متوقع نمبر: {round(avg * 1.15, 2)}x")
        with col2:
            if st.button('🗑️ CLEAR HISTORY'):
                if os.path.exists(DB_FILE):
                    os.remove(DB_FILE)
                st.rerun()

        fig = go.Figure(go.Scatter(x=g_data['Time'], y=g_data['Multiplier'], mode='lines+markers', line=dict(color='#00ffcc', width=3)))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("🛰️ اسکینر کا انتظار ہے... گیم شروع کریں اور اسکینر ایکٹیویٹ کریں۔")
        
