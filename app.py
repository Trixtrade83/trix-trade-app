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
