import os
import streamlit as st
import base64

script_dir = os.path.dirname(os.path.abspath(__file__))

background_image_path = os.path.join(script_dir, "images", "back.png")
font_path = os.path.join(script_dir, "fonts", "18 Khebrat Musamim Bold.ttf")

with open(background_image_path, "rb") as f:
    bg_bytes = f.read()
bg_base64 = base64.b64encode(bg_bytes).decode()

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

slides = ["intro", "start", "why_plant", "solution1", "follow_up", "twaiq", "solution2"]

if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0

slide = slides[st.session_state.slide_index]

if slide == "intro":
    st.markdown('<div class="custom-title">🌱 غرسة</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="custom-text"> : قال رسول الله ﷺ <br><em>'
        'ما من مسلمٍ يغرسُ غرساً أو يزرعُ زرعاً فيأكلُ منه طيرٌ أو إنسانٌ أو بهيمةٌ إلاَّ كان له به صدقة'
        '</em></div>', unsafe_allow_html=True
    )

elif slide == "start":
    st.markdown('<div class="custom-subtitle">هل فكرت تزرع؟</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="custom-text">
    هل قد فكرت إنك تزرع نبتة؟<br>
    شفت تربة بزاوية البيت وقلت: ودي أزرع شي<br>
    بس ما أدري وش يناسبها؟ زينة؟ شي يؤكل؟<br>
    .الرغبة موجودة… بس البداية مو واضحة
    </div>
    """, unsafe_allow_html=True)

elif slide == "why_plant":
    st.markdown('<div class="custom-subtitle">ليه نزرع؟ وهل كل تربة تنفع؟</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="custom-text">
    ناس تزرع لأنها تحب الخضرة<br>
    وناس عشان النعناع، الريحان، أو الراحة النفسية<br>
    لكن… مو كل تربة تنفع لكل نبتة<br>
    .وهذا اللي يخلي كثير من المحاولات تفشل
    </div>
    """, unsafe_allow_html=True)

elif slide == "solution1":
    st.markdown('<div class="custom-subtitle">غرسة تساعدك تبدأ صح</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="custom-text">
    :وهنا نبدأ أول خطوة في غرسة<br>
    ، 📸 صوّر لنا التربة<br>
    وإحنا نرشح لك أنسب النباتات تعيش فيها<br>
    .غرسة تعطيك البداية الصح
    </div>
    """, unsafe_allow_html=True)

elif slide == "follow_up":
    st.markdown('<div class="custom-subtitle">مو بس تزرع… لازم تتابع</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="custom-text">
    الزراعة مو بس غرس<br>
    كثير يزرع وينسى يتابع<br>
    والنبتة تبدأ تذبل… وما أحد يلاحظ<br>
    . وكل هذا يبدأ من ورقة وحدة فقط
    </div>
    """, unsafe_allow_html=True)

elif slide == "twaiq":
    st.markdown('<div class="custom-subtitle">نباتات طويق تتكلم</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="custom-text">
    ،نمر من طويق كل يوم<br>
    .ونشوف نباتات تتغير يوم بعد يوم<br>
    </div>
    """, unsafe_allow_html=True)
    tuwaiq_path = os.path.join(script_dir, "images", "Tuwaiq_shatlah.png")
    st.image(tuwaiq_path, caption="ممر طويق")

elif slide == "solution2":
    st.markdown('<div class="custom-subtitle">غرسة تساعدك تفهمها</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="custom-text">
    لاحظت شي غريب بورقة نبتتك؟<br>
    غرسة تقدر تعرف لك وش المشكلة<br>
    ،📸 بس صوّر الورقة<br>
    .وإحنا نقول لك اسم المرض مباشرة
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><div style='text-align: center;'>", unsafe_allow_html=True)
col_a, col_prev, col_next, col_b = st.columns([2, 1, 1, 2])
with col_prev:
    if st.button("⬅️ السابق"):
        st.session_state.slide_index = max(0, st.session_state.slide_index - 1)
        st.rerun()
with col_next:
    if st.button("التالي ➡️"):
        st.session_state.slide_index = min(len(slides) - 1, st.session_state.slide_index + 1)
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)