# 🌱 Gharsa: AI-Powered Crop and Soil Advisor

Gharsa (غرسة) is an AI-driven tool designed to empower agriculture enthusiasts and gardeners by providing insights into soil classification, crop recommendations, and early detection of plant diseases using cutting-edge computer vision technology.

---

## 📋 Table of Contents
1. [About the Project](#-about-the-project)
2. [Features](#-features)
3. [How It Works](#-how-it-works)
4. [Project Structure](#-project-structure)
5. [Getting Started](#-getting-started)
6. [Technologies Used](#-technologies-used)
7. [Team Members](#-team-members)


---

## 📖 About the Project

Gharsa aims to assist users with limited agricultural knowledge or resources by offering:
1. **Soil Classification & Crop Recommendations**: Upload a soil image to classify its type and receive crop suggestions.
2. **Plant Disease Detection**: Upload a leaf image to detect diseases like burns or spots/rots and get actionable insights.

---

## ✨ Features

### 1. Soil Classification & Crop Recommendation
- **Upload Soil Image**: Classify soil types using a Convolutional Neural Network (CNN).
- **Crop Suggestions**: Recommend suitable crops based on soil type and agricultural best practices.

Supported Soil Types:
- Alluvial
- Clay
- Loam
- Red
- Black

### 2. Leaf Disease Detection
- **Upload Leaf Image**: Detect diseases using YOLOv8.
- **Disease Types**:
  - Burns
  - Spots/Rots
- **Actionable Insights**: Identify whether immediate action is needed to save the plant.

---

## 🛠 How It Works

1. **Soil Classification**:
   - Upload a soil image.
   - The system uses a trained CNN model to classify the soil type.
   - Receive crop recommendations based on the classification.

2. **Leaf Disease Detection**:
   - Upload a close-up image of a single leaf.
   - YOLOv8 detects diseases like burns or spots/rots.
   - Get actionable insights to maintain plant health.

---
## 📂 Project Structure

```text
Gharsa/
├── backend/                        # Backend API using FastAPI
│   ├── fastapi_app.py             # Main FastAPI application
│   ├── models/                    # Pre-trained models
│   │   ├── efficientnet_model_soils2.keras
│   │   └── yolov8s_custom.pt
│   └── __pycache__/               # Compiled Python files
│
├── frontend/                      # Frontend application using Streamlit
│   ├── Gharsa.py                  # Main Streamlit app
│   ├── Pages/                     # Additional Streamlit pages
│   │   ├── أزرع نبتتك.py
│   │   ├── أفحص نبتتك.py
│   │   └── الأعضاء.py
│   ├── fonts/                     # Custom fonts for UI
│   │   └── 18 Khebrat Musamim Bold.ttf
│   ├── images/                    # Sample images for testing
│   │   ├── burn3.jpg
│   │   └── back.png
│
├── notebooks/                     # Jupyter Notebooks for experimentation
│   ├── soil_mAP 85_EfficientNetB0.ipynb
│   └── plant_diseases_more_adjucments.ipynb
│
├── README.md                      # Project documentation
├── requirements.txt               # Python dependencies
└── .gitignore                     # Git ignore rules
```

---


## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Virtual Environment (recommended)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/gharsa.git
   cd gharsa

2. install dependicies:
    ```bash
    pip install -r requirements.txt

3. Run the FastAPI backend:
    ```bash
    uvicorn backend.fastapi_app:app --reload --host 127.0.0.1 --port 8001

4. Run the Streamlit frontend:
    ```bash
    streamlit run frontend/Gharsa.py

---

## 🛠 Technologies Used
- **FastAPI**: Backend API for handling requests.
- **Streamlit**: Frontend for user interaction.
- **TensorFlow/Keras**: For soil classification using CNN.
- **YOLOv8**: For leaf disease detection.
- **OpenCV**: For image preprocessing.
- **Python**: Core programming language.

---
## 👩‍💻 Team Members

- Abdulaziz Alfrayan
- Rahaf Masmali
- Renad Alajmi
- Abdullah Alzahrani
- Abdulamohsen Aldughaym