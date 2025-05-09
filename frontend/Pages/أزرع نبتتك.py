import streamlit as st
import requests
from PIL import Image
import base64
import difflib
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
        text-align: right;
        margin: 30px 60px;
        line-height: 2;
    }}
    .custom-subtitle {{
        font-family: 'Khebrat', sans-serif;
        font-size: 35px;
        text-align: right;
        margin-top: 50px;
    }}
    .custom-title {{
        font-family: 'Khebrat', sans-serif;
        font-size: 100px;
        text-align: right;
        margin-top: 40px;
    }}
    .custom-colored-title {{
    font-family: 'Khebrat', sans-serif;
    font-size: 90px;
    text-align: right;
    direction: rtl;
    color: #4d0d0d;
    margin-top: 40px;
    }}
    </style>
    """
st.markdown(style, unsafe_allow_html=True)


st.markdown("<div class='custom-colored-title'>🌱 ازرع نبتتك !!</div>", unsafe_allow_html=True)


st.markdown("<div class = 'custom-subtitle'> : 📸 أرفع صورة التربة </div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("اختر صورة", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="🖼️ الصورة المرفوعة", use_container_width=True)

    if st.button("🔍 تصنيف التربة"):
        with st.spinner("جارٍ تحليل التربة..."):

            
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/predict",  
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

                st.markdown(f"""
                            <div style = 'text-align: right;'>
                            <h3>🌾 نوع التربة: <b>{predicted_class_ar}</b></h3>
                            </div>
                            """, unsafe_allow_html=True)

                
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
                        st.markdown("<div style = 'text-align: right;'> <h3> :🌿 التوصيات المقترحة </h3> </div>", unsafe_allow_html = True)
                        for rec in matched_recs:
                            st.markdown(f"""
                                        <div style="text-align: right;">
                                            ✅ <b>النبات:</b> {rec['plant']}<br>
                                            🪴 <b>للتربة:</b> {rec['soil_tip']}<br>
                                            🌸 <b>للنبات:</b> {rec['plant_tip']}
                                        </div>
                                        <hr>
                                        """, unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ لا توجد توصيات لهذا النوع من التربة.")
                else:
                    st.warning("⚠️ لم يتم العثور على تطابق في التوصيات لهذا النوع من التربة.")
            else:
                st.error("❌ حدث خطأ أثناء معالجة الصورة على الخادم.")
