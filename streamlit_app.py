import streamlit as st
import requests
from PIL import Image
import pandas as pd
import base64

# --- Load background ---
with open("back.png", "rb") as f:
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

# Title
st.markdown("<h1 style='text-align:center; color:#4d0d0d;'>🌱 ازرع نباتك !!</h1>", unsafe_allow_html=True)

# Image Upload
st.markdown("### 📸 أرفع صورة التربة:")
uploaded_file = st.file_uploader("اختر صورة", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="🖼️ الصورة المرفوعة", use_column_width=True)

    if st.button("🔍 تصنيف التربة"):
        with st.spinner("جارٍ تحليل التربة..."):
            # Send image to FastAPI
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                files={"file": uploaded_file.getvalue()}
            )

            if response.status_code == 200:
                result = response.json()
                predicted_class = result["class"]
                confidence = result["confidence"]

                st.markdown(f"<h3>🌾 نوع التربة: {predicted_class} ({confidence:.2%})</h3>", unsafe_allow_html=True)

                # Recommendations from Excel
                df = pd.read_excel("recommendations dataset.xlsx")
                matches = df[df['Soil'] == predicted_class]

                if not matches.empty:
                    st.markdown("### 🌿 التوصيات لزراعتك:")
                    for plant in matches['plant'].tolist():
                        st.markdown(f"✅ {plant}")
                else:
                    st.warning("لا توجد توصيات لهذا النوع من التربة.")
            else:
                st.error("❌ فشل الاتصال بـ FastAPI.")
