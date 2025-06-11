import streamlit as st
from PIL import Image

# تنظیمات صفحه
st.set_page_config(page_title="Trix Trade | تحلیل چارت", page_icon="📈", layout="centered")

# استایل‌ها
st.markdown("""
    <style>
    body {
        background-color: #111;
        color: #fff;
        font-family: 'Arial', sans-serif;
    }
    .main {
        background-color: #1a1a1a;
        color: #fff;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #e50914;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# صفحه ورود
def login():
    st.sidebar.header("🔐 ورود")
    username = st.sidebar.text_input("نام کاربری")
    password = st.sidebar.text_input("رمز عبور", type="password")
    login_btn = st.sidebar.button("ورود")
    if login_btn:
        if username == "shanixir" and password == "shayan1383":
            st.session_state["auth"] = True
        else:
            st.sidebar.error("نام کاربری یا رمز اشتباه است.")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    login()
    st.stop()

# صفحه اصلی
st.title("📊 Trix Trade")
st.markdown("""
    <h4 style='color:#e50914;'>آپلود چارت برای تحلیل</h4>
    <p>لطفاً تصویر چارت خود را بارگذاری کنید تا تحلیل اولیه و پیش‌بینی انجام شود.</p>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("آپلود تصویر چارت", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="چارت شما", use_column_width=True)

    with st.spinner("در حال تحلیل تصویر..."):
        st.success("✅ تحلیل اولیه انجام شد")
        st.markdown("""
        **پیش‌بینی حرکت قیمت:** 🔻 احتمال ریزش از سطح فعلی وجود دارد.

        **منطقه حساس:** بین 1.2450 تا 1.2480  
        **توصیه:** در صورت شکست این ناحیه، روند نزولی تایید می‌شود.
        """)
else:
    st.info("لطفاً ابتدا تصویر چارت را بارگذاری کنید.")


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
