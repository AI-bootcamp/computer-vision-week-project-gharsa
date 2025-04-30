import streamlit as st

# -------- Page Config --------
st.set_page_config(page_title="غرسة", page_icon="🌱", layout="centered")

# -------- Global CSS --------
st.markdown(
    """
    <style>
    /* Hide Streamlit default header and footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        background: #e4e7da;
        padding-top: 1rem;
        color: #212121;
        font-family: 'Segoe UI', sans-serif;
    }

    h1 {
        color: #191a1f !important;
        text-align: center;
        font-size: 2.3rem;
        margin-bottom: 10px;
    }

    p {
        text-align: center;
        font-size: 1.1rem;
        color: #5d6d7e;
        margin-top: 10px;
    }

    .main-card {
        background: none;
        padding: 0;
        border-radius: 12px;
        max-width: 700px;
        margin: auto;
    }

    .centered {
        text-align: center;
    }

    img {
        margin-bottom: 20px;
    }

    /* Updated Sidebar CSS using stable selectors */
    [data-testid="stSidebar"] {
        background-color: #708ba1;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------- Page Content --------
st.markdown("<div class='main-card'>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="centered">
        <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2s0NWk3bXhzY3h1Y2oxbHI3czRnc2NkYXIwdTRraXk1Y3dsOHI2cCZlcD12MV9zdGlja2Vyc19zZWFyY2gmY3Q9cw/3ov9k2Dg0K9otunRWo/giphy.gif"
             alt="Salesman GIF" width="180" style="margin-bottom: 10px;">
        <h1>&nbsp;&nbsp;CarInfo</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p><strong>What is this site?</strong></p>
    <p>
        Our web app helps you estimate a fair market price for your used car by using machine‑learning models trained on thousands of data.
        <br><br>
        Head over to <strong>Price Prediction</strong> to enter your car's details and get an instant estimate, or visit <strong>About Us</strong> to learn more about the team.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)
