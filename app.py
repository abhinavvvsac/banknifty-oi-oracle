import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px

# Safe import pandas_ta
try:
    import pandas_ta as ta
    HAS_TA = True
except Exception:
    HAS_TA = False

st.set_page_config(page_title="BankNifty OI Oracle", layout="wide")
st.title("📊 BankNifty OI Oracle Dashboard")

st.markdown("#### लाइव डेटा (Demo Mode)")

# Fetch BankNifty 1-minute data
data = yf.download("^NSEBANK", period="1d", interval="1m")
if data.empty:
    st.error("डेटा नहीं मिला, बाद में फिर ट्राई करें।")
    st.stop()

# Plot Close Price
fig = px.line(data, x=data.index, y="Close", title="BankNifty Live Close Price")
st.plotly_chart(fig, use_container_width=True)

# Add RSI if pandas_ta is available
if HAS_TA:
    data["RSI_14"] = ta.rsi(data["Close"], length=14)
    st.line_chart(data["RSI_14"], height=200, use_container_width=True)
else:
    st.warning("Technical indicators load नहीं हुए (pandas_ta): Skipping RSI.")

# Final bias demo
st.success("🔮 Directional Bias: CALL suggested (Demo Data)", icon="✅")
