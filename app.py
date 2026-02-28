import streamlit as st
import pandas as pd
import os
import base64
import json
import plotly.graph_objects as go
from datetime import datetime

# --- بنیادی سیٹنگز ---
st.set_page_config(page_title="Abbas Master Bot", layout="wide")
DB_FILE = "master_database.csv"
K = "x7k9p2m4q8r1t5v3n6z0y"

# --- ڈیٹا ڈی کوڈ کرنے کا فنکشن ---
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
        if not os.path.isfile(DB_FILE):
            df_new.to_csv(DB_FILE, index=False)
        else:
            df_new.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- ڈیش بورڈ ڈیزائن ---
st.title("💎 ABBAS MASTER PREDICTOR")

if os.path.isfile(DB_FILE):
    df = pd.read_csv(DB_FILE)
    game_list = df['Game'].unique()
    selected_game = st.sidebar.selectbox("Select Game", game_list)
    g_data = df[df['Game'] == selected_game]
    last_val = g_data['Multiplier'].iloc[-1]

    # اڑتا ہوا جہاز اور لائیو نمبر
    st.markdown(f"""
        <div style="background: black; padding: 20px; border-radius: 15px; border: 2px solid #00ffcc; text-align: center;">
            <h1 style="color: #00ffcc; font-size: 50px; margin: 0;">{last_val}x</h1>
            <div style="font-size: 40px; animation: move 2s infinite alternate;">✈️</div>
            <style> @keyframes move {{ from {{transform: translateX(-20px);}} to {{transform: translateX(20px);}} }} </style>
        </div>
    """, unsafe_allow_key=True)

    # پریڈکشن بٹن
    st.write("---")
    if st.button('🚀 GET NEXT SIGNAL'):
        avg = g_data['Multiplier'].tail(10).mean()
        target = round(avg * 1.2, 2)
        st.info(f"اگلا متوقع ٹارگٹ: {target}x")
    st.write("---")

    # گراف
    fig = go.Figure(go.Scatter(y=g_data['Multiplier'].tail(20), mode='lines+markers', line=dict(color='#00ffcc')))
    fig.update_layout(title="راؤنڈز کی ہسٹری", paper_bgcolor='black', plot_bgcolor='black', font=dict(color='white'))
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("انتظار کریں... جیسے ہی گیم سے پہلا نمبر آئے گا، یہاں سب کچھ نظر آ جائے گا۔")
    
