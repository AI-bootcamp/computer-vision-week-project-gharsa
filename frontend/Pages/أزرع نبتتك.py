import streamlit as st
import requests
from PIL import Image
import base64
import difflib
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)  # Move one level up
background_image_path = os.path.join(parent_dir, "images", "Gharsa_background.png")

font_path = os.path.join(parent_dir, "fonts", "18 Khebrat Musamim Bold.ttf")

# Read the font file
with open(font_path, "rb") as font_file:
    font_base64 = base64.b64encode(font_file.read()).decode()

    
with open(background_image_path, "rb") as f:
    bg_bytes = f.read()
bg_base64 = base64.b64encode(bg_bytes).decode()

st.markdown(
    
    f"""
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
    """,
    unsafe_allow_html=True 

)


st.markdown("<h1 style='text-align:center; color:#4d0d0d;'>🌱 ازرع نباتك !!</h1>", unsafe_allow_html=True)


st.markdown("### 📸 أرفع صورة التربة:")
uploaded_file = st.file_uploader("اختر صورة", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="🖼️ الصورة المرفوعة", use_container_width=True)

    if st.button("🔍 تصنيف التربة"):
        with st.spinner("جارٍ تحليل التربة..."):

            
            try:
                response = requests.post(
                    "http://127.0.0.1:8001/predict",  
                    files={"file": uploaded_file.getvalue()}
                )
            except Exception as e:
                st.error("❌ لم يتم الاتصال بـ FastAPI. تأكد من تشغيل الخادم على المنفذ 8001.")
                st.stop()

            
            if response.status_code == 200:
                result = response.json()
                predicted_class = result["class"]
                confidence = result["confidence"]

                soil_translation = {
                    "Alluvial soil": "تربة فيضية",
                    "Alluvial soil": "تربة الرسوبية",
                    "Black Soil": "تربة سوداء",
                    "Clay soil": "تربة طينية",
                    "Red soil": "تربة حمراء",
                    "loam": "تربة طميية",
                    "sandy": "تربة رملية"
                }
                predicted_class_ar = soil_translation.get(predicted_class, predicted_class)

                st.markdown(f"<h3>🌾 نوع التربة: <b>{predicted_class_ar}</b></h3>", unsafe_allow_html=True)

                
                recommendations_data = [
                    {"soil": "تربة طميية", "plant": "الخضروات، التفاح، العنب، الخوخ، القمح، الشعير، الزهور", "soil_tip": "أضف مواد عضوية بانتظام وقلل الري الزائد.", "plant_tip": "ازرعها في تربة طميية جيدة التصريف وإضاءة غير مباشرة."},
                    {"soil": "تربة حمراء", "plant": " الفول السوداني، البطاطا الحلوة، الدخن، البقوليات، الكركم، الموز", "soil_tip": "عزز خصوبة التربة الحمراء بإضافة الكمبوست والملش.", "plant_tip": "اخلطها بالسماد لتحسين النمو."},
                    {"soil": "تربة طينية", "plant": " الأرز، الكرنب، البروكلي، الكرفس، البرسيم", "soil_tip": "اخلطها بالرمل أو البرلايت لتحسين التصريف.", "plant_tip": "تربة غنية تحافظ على الرطوبة تناسب الكالاديوم."},
                    {"soil": "تربة سوداء", "plant": "القطن، عباد الشمس، الحمص، الدخن، الذرة البيضاء", "soil_tip": "تربة غنية ولكن تحتاج تحسين تصريف باستخدام بيرلايت.", "plant_tip": "أضف كمبوست للحفاظ على الرطوبة والتغذية."},
                    {"soil": "تربة فيضية", "plant": "الأرز، القمح، قصب السكر، الذرة، القطن، الطماطم، البطاطس، الورقيات", "soil_tip": "تربة ممتازة لكنها تحتفظ بالماء، أضف رمل لتحسين التصريف.", "plant_tip": "ينمو الريحان جيدًا عند تحسين التصريف وإضافة كمبوست بسيط."},
                    {"soil": "تربة رملية", "plant": "الجزر، الفول السوداني، البطيخ، البطاطا، البصل، الصبار", "soil_tip": "تربة خفيفة سريعة التصريف، أضف قليل من الكمبوست فقط.", "plant_tip": "تحتاج لتربة جافة وأشعة شمس مباشرة."}
                ]

                
                soil_names = list(set(r["soil"] for r in recommendations_data))
                matched_soil = difflib.get_close_matches(predicted_class_ar, soil_names, n=1, cutoff=0.4)

                if matched_soil:
                    matched_soil = matched_soil[0]
                    matched_recs = [r for r in recommendations_data if r["soil"] == matched_soil]

                    if matched_recs:
                        st.markdown("### 🌿 التوصيات المقترحة:")
                        for rec in matched_recs:
                            st.markdown(f"✅ <b>النبات:</b> {rec['plant']}", unsafe_allow_html=True)
                            st.markdown(f" 🪴 <b>للتربة:</b> {rec['soil_tip']}", unsafe_allow_html=True)
                            st.markdown(f" 🌸 <b>للنبات:</b> {rec['plant_tip']}", unsafe_allow_html=True)
                            st.markdown("---")
                    else:
                        st.warning("⚠️ لا توجد توصيات لهذا النوع من التربة.")
                else:
                    st.warning("⚠️ لم يتم العثور على تطابق في التوصيات لهذا النوع من التربة.")
            else:
                st.error("❌ حدث خطأ أثناء معالجة الصورة على الخادم.")