
import streamlit as st
from PIL import Image
import numpy as np
import io
import cv2

# --- UI Setup ---
st.set_page_config(page_title="Trix Trade Analyzer", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Logo and Title ---
st.markdown("<h2 style='color:red;'>به سایت تحلیل Trix_Trade خوش آمدید</h2>", unsafe_allow_html=True)

# --- Image Upload ---
st.subheader("📤 تصویر چارت خود را آپلود کنید:")
uploaded_file = st.file_uploader("فرمت قابل قبول: PNG, JPG", type=["png", "jpg", "jpeg"])

# --- Analysis Placeholder ---
def analyze_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80, minLineLength=50, maxLineGap=10)

    trend = "نامشخص"
    if lines is not None:
        avg_slope = np.mean([(y2 - y1)/(x2 - x1 + 0.01) for x1, y1, x2, y2 in lines[:, 0]])
        if avg_slope > 0.2:
            trend = "📈 روند کلی صعودی است"
        elif avg_slope < -0.2:
            trend = "📉 روند کلی نزولی است"
        else:
            trend = "🔁 روند خنثی یا اصلاحی است"
    return trend

# --- Main App ---
if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    st.image(image, caption="چارت آپلود شده", use_column_width=True)

    st.subheader("🔎 تحلیل اولیه:")
    result = analyze_image(image)
    st.success(result)

    st.info("⚠️ تحلیل سطحی است. نسخه حرفه‌ای با ابزارهای بیشتر در حال توسعه است.")
else:
    st.warning("لطفاً یک تصویر چارت آپلود کنید.")
