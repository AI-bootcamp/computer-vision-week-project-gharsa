import streamlit as st
from Home import show_home
from Team import show_team 

page = st.sidebar.radio(" اختر الصفحة", [
    " الصفحة الرئيسية", " ازرع نبتتك", " افحص نبتتك", " فريق العمل"
])

if page == " الصفحة الرئيسية":
    show_home()
elif page == " ازرع نبتتك":
    show_plant()
elif page == " افحص نبتتك":
    show_check()
elif page == " فريق العمل":
    show_team()