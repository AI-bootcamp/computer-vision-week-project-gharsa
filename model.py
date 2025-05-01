from ultralytics import YOLO
import numpy

loaded_model = YOLO("yolov8s_Custom1.pt")


def predict(photo: numpy array) -> numpy array:

    return labeled_photo