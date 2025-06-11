import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ta
from io import StringIO

st.set_page_config(page_title="Trix Trade", layout="wide")

st.title("📊 تحلیل تکنیکال خودکار - Trix Trade")
st.markdown("آپلود فایل CSV چارت (دارای ستون‌های `Date`, `Open`, `High`, `Low`, `Close`, `Volume`)")

uploaded_file = st.file_uploader("فایل چارت را آپلود کنید", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # پاکسازی و آماده‌سازی
    df.columns = df.columns.str.strip()
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    st.subheader("📈 نمودار قیمت")
    st.line_chart(df['Close'])

    # محاسبه اندیکاتورها
    df['rsi'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    df['macd'] = ta.trend.MACD(df['Close']).macd_diff()
    df['ma50'] = df['Close'].rolling(window=50).mean()
    df['ma200'] = df['Close'].rolling(window=200).mean()

    st.subheader("📉 اندیکاتورها")
    fig, ax = plt.subplots()
    df[['Close', 'ma50', 'ma200']].plot(ax=ax)
    plt.title("Moving Averages")
    st.pyplot(fig)

    st.subheader("📌 تحلیل اولیه")
    last_rsi = df['rsi'].iloc[-1]
    last_macd = df['macd'].iloc[-1]
    last_price = df['Close'].iloc[-1]
    ma50 = df['ma50'].iloc[-1]
    ma200 = df['ma200'].iloc[-1]

    signal = "🔍 تحلیل اولیه: "

    # تصمیم‌گیری ساده بر اساس وضعیت اندیکاتورها
    if last_rsi < 30:
        signal += "اشباع فروش (احتمال برگشت قیمت). "
    elif last_rsi > 70:
        signal += "اشباع خرید (احتمال اصلاح قیمت). "
    else:
        signal += "RSI نرمال. "

    if last_macd > 0:
        signal += "قدرت صعودی در MACD. "
    else:
        signal += "فشار نزولی در MACD. "

    if last_price > ma50 and ma50 > ma200:
        signal += "روند صعودی تایید شده."
    elif last_price < ma50 and ma50 < ma200:
        signal += "روند نزولی تایید شده."
    else:
        signal += "بازار در حالت رِنج یا تغییر روند است."

    st.success(signal)

    # سیگنال‌های احتمالی
    st.subheader("🎯 نقاط احتمالی ورود و خروج")
    if last_rsi < 35 and last_macd > 0:
        st.info(f"✅ نقطه ورود احتمالی: {last_price:.2f}")
        st.warning(f"🛑 حد ضرر: {last_price * 0.97:.2f}")
        st.success(f"🎯 تارگت: {last_price * 1.05:.2f}")
    else:
        st.info("در حال حاضر شرایط مناسب برای ورود دیده نمی‌شود.")

else:
    st.warning("برای شروع تحلیل، لطفاً یک فایل چارت CSV آپلود کنید.")
