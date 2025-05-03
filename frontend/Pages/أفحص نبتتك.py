import streamlit as st
import numpy as np
import cv2
import requests
from PIL import Image
import base64
import difflib
import io
import os


script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute paths
background_image_path = os.path.join(script_dir, "..", "images", "back.png")
font_path = os.path.join(script_dir, "..", "fonts", "18 Khebrat Musamim Bold.ttf")

# Read the background image
with open(background_image_path, "rb") as f:
    bg_bytes = f.read()
bg_base64 = base64.b64encode(bg_bytes).decode()

# Read the font file
with open(font_path, "rb") as font_file:
    font_base64 = base64.b64encode(font_file.read()).decode()

style = f"""
    <style>
    @font-face {{
        font-family: 'Khebrat';
        src: url("data:font/ttf;base64,{font_base64}") format('truetype');
    }}
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        font-family: 'Khebrat', sans-serif;
        color: #222;
    }}
    .custom-text {{
        font-family: 'Khebrat', sans-serif;
        font-size: 35px;
        text-align: center;
        margin: 30px 60px;
        line-height: 2;
    }}
    .custom-subtitle {{
        font-family: 'Khebrat', sans-serif;
        font-size: 42px;
        text-align: center;
        margin-top: 50px;
    }}
    .custom-title {{
        font-family: 'Khebrat', sans-serif;
        font-size: 100px;
        text-align: center;
        margin-top: 40px;
    }}
    </style>
    """
st.markdown(style, unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#4d0d0d;'>🌱 افحص نبتتك !!</h1>", unsafe_allow_html=True)


st.markdown("### 📸 أرفع صورة النبتة:")
uploaded_file = st.file_uploader("اختر صورة", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # عرض الصورة الأصلية
    st.image(uploaded_file, caption="🖼️ الصورة المرفوعة", use_container_width=True)

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

            # show the image without caption
            st.image(annotated, use_container_width=True)

            # 2) translate class names
            class_translation = {
                "rot-spot": "تعفن/بقعة",
                "no rot-spot or burns":   "لا يوجد حرق أو تعفن/بقعة",
                "burn":      "حرق"
            }
            predicted = data["class"]
            predicted_ar = class_translation.get(predicted, predicted)

            # 3) big header with inline HTML (centred, large, colored)
            st.markdown(
                f"<h1 style='text-align:center; color:#d62828;'>🔬 التشخيص: <strong>{predicted_ar}</strong></h1>",
                unsafe_allow_html=True
            )

            # 4) recommendations per class
            recommendations = {
                "تعفن/بقعة": [
                    "✅ أزل الأجزاء المتعفنة برفق واحرص على التهوية الجيدة.",
                    "✅ قلل من رطوبة التربة واسمح لها أن تجف قليلًا قبل الري مجددًا.",
                    "✅ استخدم مبيدًا فطريًا مناسبًا إذا استمر التعفن."
                ],
                "لا يوجد حرق أو تعفن/بقعة": [
                    "🌱 نباتك بصحة جيدة! حافظ على روتين ري معتدل.",
                    "🌱 تأكد من وصول الضوء الكافي وتجنب التعرض المباشر للشمس القوية.",
                    "🌱 زد التسميد العضوي مرة كل شهر لتحفيز النمو."
                ],
                "حرق": [
                    "🔥 قص الأوراق المحروقة لتشجيع نمو جديدة.",
                    "🔥 انقل النبات إلى مكان أقل سطوعًا أو استخدم ستارة خفيفة.",
                    "🔥 تجنب رَشِّ الماء على الأوراق في ساعات الظهيرة."
                ]
            }

            recs = recommendations.get(predicted_ar)
            if recs:
                st.markdown("### 🌿 التوصيات المقترحة:")
                for tip in recs:
                    st.markdown(f"- {tip}", unsafe_allow_html=True)
            else:
                st.warning("⚠️ لا توجد توصيات متاحة لهذه الحالة.")