import streamlit as st
import base64


with open("frontend/images/Gharsa_background.png", "rb") as f:
    bg_bytes = f.read()
bg_base64 = base64.b64encode(bg_bytes).decode()


with open("frontend/fonts/18 Khebrat Musamim Bold.ttf", "rb") as font_file:
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
    font-size: 32px;
    text-align: center;
    margin: 40px 60px;
    line-height: 2;
}}
.custom-subtitle {{
    font-family: 'Khebrat', sans-serif;
    font-size: 50px;
    text-align: center;
    margin-top: 40px;
}}
</style>
"""
st.markdown(style, unsafe_allow_html=True)


st.markdown('<div class="custom-subtitle">🌿 فريق غرسة</div>', unsafe_allow_html=True)

st.markdown("""
<div class="custom-text">
    ،كانت بذرة<br>
فنمَت بنقاشنا، وسُقيت بعملنا، وأثمرت بتعاوننا.<br>
: وهؤلاء من كانوا جزءًا من رحلتها <br>
🌱 رهف مسملي<br>
🌱 عبدالمحسن الدغيم<br>
🌱 رناد العجمي<br>
🌱 عبدالعزيز الفريان<br>
🌱 عبدالله الزهراني
</div>
""", unsafe_allow_html=True)