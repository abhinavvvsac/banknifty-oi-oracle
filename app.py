import streamlit as st
import pandas as pd
import yfinance as yf
import pandas-ta as ta
import time

st.set_page_config(page_title="BankNifty OI Oracle", layout="wide")
st.markdown("<h1 style='text-align:center'>🔮 BankNifty OI Oracle</h1>", unsafe_allow_html=True)

mode = st.sidebar.radio("⚙️ सिग्नल मोड", ["Safe", "Aggressive", "Combo"])
voice_on = st.sidebar.checkbox("🔊 आवाज़ सुनो", True)
st.sidebar.markdown("Made for Abhinav Sachan")

@st.cache(ttl=60)
def fetch_data():
    df = yf.download("^NSEBANK", period="1d", interval="1m")
    df["EMA9"] = ta.ema(df["Close"], length=9)
    df["EMA21"] = ta.ema(df["Close"], length=21)
    # … बाकी आपके लॉजिक यहाँ एड करो …
    return df

df = fetch_data()
st.subheader("📈 Price & Indicators")
st.line_chart(df[["Close", "EMA9", "EMA21"]])

# … सारे वर्किंग फीचर्स इधर एड करो …

def compute_verdict(df):
    last, ema9, ema21 = df["Close"].iloc[-1], df["EMA9"].iloc[-1], df["EMA21"].iloc[-1]
    if last > ema9 > ema21:
        return "📈 कॉल लेना सही रहेगा", 85
    else:
        return "📉 पुट लेना बेहतर रहेगा", 75

verdict, conf = compute_verdict(df)
st.markdown(f"## 🔮 अंतिम निर्णय: **{verdict}** (विश्वास: {conf}%)")

if voice_on:
    st.components.v1.html(f"""
    <script>
      let msg = new SpeechSynthesisUtterance("{verdict}");
      window.speechSynthesis.speak(msg);
    </script>
    """, height=0)

# Auto-refresh
time.sleep(5)
st.experimental_rerun()
