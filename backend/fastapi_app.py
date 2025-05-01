from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import os

app = FastAPI()

# CORS for Streamlit access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained Keras model
model = load_model("backend/models/efficientnet_model_soils2.keras")
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

    preds = model.predict(img)
    class_index = int(np.argmax(preds))
    class_name = class_names[class_index]
    confidence = float(np.max(preds))

    return {"class": class_name, "confidence": confidence}
