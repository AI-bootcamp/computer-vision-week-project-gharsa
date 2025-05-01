# app.py

import streamlit as st
import numpy as np
import cv2
from ultralytics import YOLO

# 1. Load your model once
model = YOLO("yolov8s_Custom1.pt")

def predict(photo: np.ndarray) -> np.ndarray:
    """
    photo: a BGR image as a NumPy array (HxWx3)
    returns: the same image annotated with boxes & patched labels
    """
    # Run inference
    results = model(photo)
    res = results[0]

    # Patch any 'spot' or 'rot' names to 'rot-spot'
    for cls_idx, cls_name in res.names.items():
        if cls_name in ("spot", "rot"):
            res.names[cls_idx] = "rot-spot"

    # Draw boxes + labels onto a copy of the input
    annotated = res.plot()  # this returns an HxWx3 NumPy array
    return annotated

# 2. Streamlit UI
st.title("🍃 Leaf Disease Detector")

uploaded_file = st.file_uploader(
    "Upload a leaf image (jpg/png)", type=["jpg", "jpeg", "png"]
)
if uploaded_file is not None:
    # Read raw bytes from the uploader and convert to NumPy array
    file_bytes = np.frombuffer(uploaded_file.read(), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # BGR
    
    # 3. Get your annotated result
    labeled_img = predict(img)
    
    # Convert BGR→RGB for correct display in Streamlit
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_BGR2RGB)
    
    st.image(
        labeled_img,
        caption="Detected diseases (rot-spot merged)",
        use_column_width=True
    )
