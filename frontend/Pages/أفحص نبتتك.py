import streamlit as st
import numpy as np
import cv2
import requests
from PIL import Image
import base64
import difflib
import io



with open("frontend/images/back.png", "rb") as f:
    bg_bytes = f.read()
bg_base64 = base64.b64encode(bg_bytes).decode()

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        font-family: 'Cairo', sans-serif;
        color: #222;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown("<h1 style='text-align:center; color:#4d0d0d;'>🌱 افحص نبتتك !!</h1>", unsafe_allow_html=True)


st.markdown("### 📸 أرفع صورة النبتة:")
uploaded_file = st.file_uploader("اختر صورة", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # عرض الصورة الأصلية
    st.image(uploaded_file, caption="🖼️ الصورة المرفوعة", use_column_width=True)

    if st.button("🔍 حلل النبتة"):
        with st.spinner("جارٍ تحليل النبتة..."):
            # 1. اقرأ الملف المرفوع كـ bytes
            file_bytes = uploaded_file.getvalue()

            # 2. أرسل الصورة إلى FastAPI وانتظر JSON بالـ class + confidence + base64 image
            try:
                resp = requests.post(
                    "http://127.0.0.1:8000/detect",
                    files={"file": file_bytes}
                )
                resp.raise_for_status()
            except Exception as e:
                st.error("❌ لم يتم الاتصال بـ FastAPI أو حدث خطأ أثناء المعالجة.")
                st.exception(e)
                st.stop()

            # 3. فكّ الـBase64 وعرض الصورة المعلمة
            data = resp.json()
            img_bytes = base64.b64decode(data["image"])
            annotated = Image.open(io.BytesIO(img_bytes))
            st.image(annotated, caption=f"🔬 تشخيص: {data['class']}", use_column_width=True)