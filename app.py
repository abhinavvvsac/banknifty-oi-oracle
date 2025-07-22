import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="BankNifty OI Oracle", layout="wide")
st.title("📊 BankNifty OI Oracle Dashboard (Demo)")

# Fetch BankNifty 1-minute data
data = yf.download("^NSEBANK", period="1d", interval="1m")
if data.empty:
    st.error("डेटा नहीं मिला; बाद में फिर ट्राई करें।")
    st.stop()

# Plot Close Price
fig = px.line(data, x=data.index, y="Close", title="BankNifty Live Close Price")
st.plotly_chart(fig, use_container_width=True)

st.markdown("### 📈 RSI (14) Indicator")

# Manual RSI calculation
def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.ewm(com=period - 1, adjust=True).mean()
    ma_down = down.ewm(com=period - 1, adjust=True).mean()
    rs = ma_up / ma_down
    rsi = 100 - (100 / (1 + rs))
    return rsi

data["RSI_14"] = compute_rsi(data["Close"], period=14)

st.line_chart(data["RSI_14"], height=200, use_container_width=True)

# Demo directional bias
st.success("🔮 Directional Bias (Demo): CALL suggested", icon="✅")
