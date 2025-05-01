import streamlit as st
from model import *

st.title("🍃 Leaf Disease Detector")

uploaded = st.file_uploader("Upload a leaf image", type=["jpg","jpeg","png"])
if uploaded:
    data = np.frombuffer(uploaded.read(), np.uint8)
    img  = cv2.imdecode(data, cv2.IMREAD_COLOR)
    out  = predict(img)
    out  = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
    st.image(out, caption="rot-spot", use_column_width=True)
