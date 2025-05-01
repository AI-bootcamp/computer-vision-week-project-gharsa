import streamlit as st
import requests
from PIL import Image
import base64
import difflib


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


st.markdown("<h1 style='text-align:center; color:#4d0d0d;'>🌱 ازرع نباتك !!</h1>", unsafe_allow_html=True)


st.markdown("### 📸 أرفع صورة التربة:")
uploaded_file = st.file_uploader("اختر صورة", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="🖼️ الصورة المرفوعة", use_column_width=True)

    if st.button("🔍 تصنيف التربة"):
        with st.spinner("جارٍ تحليل التربة..."):

            
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/predict", #<---API
                    files={"file": uploaded_file.getvalue()}
                )
            except Exception as e:
                st.error("❌ لم يتم الاتصال بـ FastAPI. تأكد من تشغيل الخادم.")
                st.stop()

            
            if response.status_code == 200:
                result = response.json()
                predicted_class = result["class"]
                confidence = result["confidence"]

                st.markdown(f"<h3>🌾 نوع التربة: <b>{predicted_class}</b> (الدقة: {confidence:.2%})</h3>", unsafe_allow_html=True)

                
                recommendations_data = [
                    {"soil": "طميية", "plant": "مونسترا", "soil_tip": "حافظ على التربة الطميية بإضافة مواد عضوية بانتظام وتجنب الإفراط في الري.", "plant_tip": "ازرع المونسترا في تربة طميية جيدة التصريف، واحرص على الإضاءة غير المباشرة."},
                    {"soil": "Red", "plant": "Pothos", "soil_tip": "قم بتحسين التربة الحمراء بإضافة السماد والملش لتخفيف التصلب وزيادة الخصوبة.", "plant_tip": "اخلط التربة الحمراء بالسماد لمساعدة نبات البوتس على النمو."},
                    {"soil": "Clay", "plant": "Caladium", "soil_tip": "اخلط التربة الطينية بالرمل أو الكمبوست لتحسين التهوية والتصريف.", "plant_tip": "تربة طينية محسّنة بالسماد تساعد الكالاديوم على الاحتفاظ بالرطوبة."},
                    {"soil": "Black", "plant": "Philodendron", "soil_tip": "رغم غناها، يمكن أن تتصلب التربة السوداء، لذا امزجها بالبيرلايت أو الرمل.", "plant_tip": "الفيلوديندرون ينمو جيدًا في تربة سوداء مضاف لها كمبوست."},
                    {"soil": "Alluvial", "plant": "الريحان و الورقيات", "soil_tip": "تربة الطمي الفيضي جيدة، لكن تحتاج تصريف جيد، امزجها برمل أو بيرلايت.", "plant_tip": "الريحان يزدهر في تربة فيضية مع تصريف جيد وقليل من السماد."},
                    {"soil": "Sandy", "plant": "Echeveria", "soil_tip": "التربة الرملية سريعة التصريف، أضف القليل من الكمبوست عند الحاجة.", "plant_tip": "الإشفيريا تحتاج تربة رملية جافة مع تعرض جيد للشمس."},
                ]

                
                soil_names = list(set(r["soil"] for r in recommendations_data))
                matched_soil = difflib.get_close_matches(predicted_class, soil_names, n=1, cutoff=0.4)

                if matched_soil:
                    matched_soil = matched_soil[0]
                    matched_recs = [r for r in recommendations_data if r["soil"] == matched_soil]

                    if matched_recs:
                        st.markdown("### 🌿 التوصيات المناسبة:")
                        for rec in matched_recs:
                            st.markdown(f"<b>✅ النبات:</b> {rec['plant']}", unsafe_allow_html=True)
                            st.markdown(f" <b>🪴 للتربة:</b> {rec['soil_tip']}", unsafe_allow_html=True)
                            st.markdown(f" <b>🌸 للنبات:</b> {rec['plant_tip']}", unsafe_allow_html=True)
                            st.markdown("---")
                    else:
                        st.warning("⚠️ لا توجد توصيات مسجلة لهذا النوع من التربة.")
                else:
                    st.warning("⚠️ لم يتم العثور على تطابق مع اسم التربة المتوقع.")
            else:
                st.error("❌ حدث خطأ في الخادم أثناء التصنيف.")
