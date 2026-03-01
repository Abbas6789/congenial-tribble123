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

# --- ڈیٹا ڈی کوڈ کرنے کا نیا اور مضبوط فنکشن ---
def decrypt(en_str):
    try:
        # یو آر ایل سے ڈیٹا صاف کرنا
        en_str = urllib.parse.unquote(en_str)
        b = base64.b64decode(en_str)
        # XOR ڈی کوڈنگ
        decrypted_bytes = bytearray()
        for i in range(len(b)):
            decrypted_bytes.append(b[i] ^ ord(K[i % len(K)]))
        
        return json.loads(decrypted_bytes.decode('utf-8'))
    except Exception as e:
        return None

# --- ڈیٹا پکڑنا اور سیو کرنا (نیو میتھڈ) ---
params = st.query_params
if 'd' in params:
    data_raw = params['d']
    sd = decrypt(data_raw)
    
    if sd:
        # ڈیٹا کو ترتیب دینا
        current_time = datetime.now().strftime("%H:%M:%S")
        game_name = sd.get('g', {}).get('h', 'Unknown Game')
        val = sd.get('i', {}).get('v', '0')
        
        try:
            multiplier = float(val)
            row = {"Time": current_time, "Game": game_name, "Multiplier": multiplier}
            df_new = pd.DataFrame([row])
            
            # فائل میں محفوظ کرنا
            if not os.path.isfile(DB_FILE):
                df_new.to_csv(DB_FILE, index=False)
            else:
                df_new.to_csv(DB_FILE, mode='a', header=False, index=False)
            
            # پیج کو ریفریش کرنا تاکہ نیا نمبر نظر آئے
            st.rerun()
        except:
            pass

# --- ڈیش بورڈ ڈیزائن ---
st.title("💎 ABBAS MASTER PREDICTOR")

if os.path.isfile(DB_FILE):
    df = pd.read_csv(DB_FILE)
    # صرف آخری 50 ریکارڈز دکھانا تاکہ ایپ تیز چلے
    df = df.tail(50)
    
    game_list = df['Game'].unique()
    selected_game = st.sidebar.selectbox("Select Game", game_list)
    g_data = df[df['Game'] == selected_game]
    
    if not g_data.empty:
        last_val = g_data['Multiplier'].iloc[-1]

        # لائیو ڈسپلے
        st.markdown(f"""
            <div style="background: #111; padding: 20px; border-radius: 15px; border: 2px solid #00ffcc; text-align: center;">
                <h3 style="color: white; margin-bottom: 5px;">LIVE MULTIPLIER</h3>
                <h1 style="color: #00ffcc; font-size: 70px; margin: 0; font-family: monospace;">{last_val}x</h1>
                <div style="font-size: 40px; animation: move 1s infinite alternate;">✈️</div>
                <style> @keyframes move {{ from {{transform: translateY(0px);}} to {{transform: translateY(-10px);}} }} </style>
            </div>
        """, unsafe_allow_key=True)

        st.write("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button('🚀 GET NEXT SIGNAL', use_container_width=True):
                avg = g_data['Multiplier'].tail(5).mean()
                prediction = round(avg * 1.15, 2)
                st.success(f"اگلا متوقع نمبر: {prediction}x")
        
        with col2:
            if st.button('🗑️ CLEAR HISTORY', use_container_width=True):
                if os.path.exists(DB_FILE):
                    os.remove(DB_FILE)
                    st.rerun()

        # گراف
        fig = go.Figure(go.Scatter(
            x=g_data['Time'], 
            y=g_data['Multiplier'], 
            mode='lines+markers', 
            line=dict(color='#00ffcc', width=3),
            marker=dict(size=10, color='white')
        ))
        fig.update_layout(
            title="گیم کی لائیو ہسٹری",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#333')
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("🛰️ اسکینر کا انتظار ہے... گیم شروع کریں اور اسکینر ایکٹیویٹ کریں۔")
        
