from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from fastapi.responses import StreamingResponse, JSONResponse
from ultralytics import YOLO
import tensorflow as tf
import numpy as np
import base64
import os
import cv2

app = FastAPI()

# CORS for Streamlit access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained soil classification Keras model and YOLO disease detection model
model_soil = load_model("backend/models/efficientnet_model_soils2.keras")
model_yolo = YOLO("backend/models/yolov8s_custom.pt")

img_size = (224, 224)

# Your class names manually listed or loaded
class_names =['Alluvial soil', 'Black Soil', 'Clay soil', 'Red soil', 'loam', 'sandy']

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    img = tf.image.decode_image(contents, channels=3)
    img = tf.image.resize(img, img_size)
    img = tf.keras.applications.efficientnet.preprocess_input(img)
    img = tf.expand_dims(img, 0)

    preds = model_soil.predict(img)
    class_index = int(np.argmax(preds))
    class_name = class_names[class_index]
    confidence = float(np.max(preds))

    return {"class": class_name, "confidence": confidence}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    # 1) اقرأ الصورة
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    photo = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 2) inference
    results = model_yolo(photo)
    res = results[0]

    # 3) دمج spot/rot → rot-spot
    for idx, nm in res.names.items():
        if nm in ("spot", "rot"):
            res.names[idx] = "rot-spot"

    # 4) استخرج صناديق الكشف، الأصناف، الثقة
    boxes       = res.boxes.xyxy.cpu().numpy().astype(int)
    class_ids   = res.boxes.cls.cpu().numpy().astype(int)
    confidences = res.boxes.conf.cpu().numpy()
    names       = res.names

    # 5) حدد التشخيص النهائي ودرجة الثقة
    if len(class_ids) == 0:
        predicted_class = "healthy"
        confidence = 1.0
    else:
        labels = [names[c] for c in class_ids]
        if "rot-spot" in labels:
            predicted_class = "rot-spot"
            idxs = [i for i, lbl in enumerate(labels) if lbl == "rot-spot"]
        elif "burn" in labels:
            predicted_class = "burn"
            idxs = [i for i, lbl in enumerate(labels) if lbl == "burn"]
        else:
            predicted_class = labels[0]
            idxs = [0]
        confidence = float(confidences[idxs].max())

    # 6) ارسم الصناديق والتسميات ديناميكياً
    img = photo.copy()
    REF_H, MIN_S, MAX_S = 50.0, 0.5, 2.0
    TF, PF = 2, 5
    font = cv2.FONT_HERSHEY_SIMPLEX

    for (x1, y1, x2, y2), cls_id in zip(boxes, class_ids):
        label = names[cls_id]
        color = (53, 56, 57)

        box_h = y2 - y1
        fs = max(MIN_S, min(box_h / REF_H, MAX_S))
        th = max(1, int(fs * TF))
        pad = int(fs * PF)

        (w, h), _ = cv2.getTextSize(label, font, fs, th)
        # الصندوق
        cv2.rectangle(img, (x1, y1), (x2, y2), color, th)
        # خلفية النص
        cv2.rectangle(img,
                      (x1, y1 - h - 2*pad),
                      (x1 + w + 2*pad, y1),
                      color, thickness=-1)
        # النص
        cv2.putText(img, label, (x1 + pad, y1 - pad),
                    font, fs, (255,255,255), th, cv2.LINE_AA)

    # 7) ترميز الصورة إلى Base64
    _, buffer = cv2.imencode(".png", img)
    img_b64 = base64.b64encode(buffer).decode("utf-8")

    # 8) أعد JSON بالتصنيف والثقة والصورة
    return JSONResponse({
        "class":     predicted_class,
        "confidence": confidence,
        "image":     img_b64
    })
