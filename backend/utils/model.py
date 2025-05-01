import cv2
import numpy as np
from ultralytics import YOLO

# load once
model = YOLO("models/yolov8s_Custom.pt")

def predict(photo: np.ndarray) -> np.ndarray:
    """
    photo: BGR HxWx3 uint8 image
    return: BGR HxWx3 uint8 annotated image with boxes + labels only
    """
    # 1) inference
    results = model(photo)
    res = results[0]

    # 2) patch names in-place
    for idx, nm in res.names.items():
        if nm in ("spot", "rot"):
            res.names[idx] = "rot-spot"

    # 3) extract detections
    boxes     = res.boxes.xyxy.cpu().numpy().astype(int)  # [[x1,y1,x2,y2],...]
    class_ids = res.boxes.cls.cpu().numpy().astype(int)
    names     = res.names

    # 4) draw
    
    img = photo.copy()

    REF_HEIGHT   = 50.0   # “box height in px” that corresponds to font_scale=1.0
    MIN_SCALE    = 0.5    # never go below this (too small to read)
    MAX_SCALE    = 2.0    # never go above this (crowds the box)
    THICKNESS_FACTOR = 2  # thickness = int(font_scale * THICKNESS_FACTOR)
    PAD_FACTOR       = 5  # padding = int(font_scale * PAD_FACTOR)

    for (x1, y1, x2, y2), cls_id in zip(boxes, class_ids):
        label = names[cls_id]
        color = (53,56,57)

        # compute box dims
        box_h = y2 - y1

        # dynamic font scale based on box height
        font_scale = box_h / REF_HEIGHT
        # clamp to [MIN_SCALE, MAX_SCALE]
        font_scale = max(MIN_SCALE, min(font_scale, MAX_SCALE))

        # derive thickness and padding from font scale
        thickness = max(1, int(font_scale * THICKNESS_FACTOR))
        pad       = int(font_scale * PAD_FACTOR)
        font      = cv2.FONT_HERSHEY_SIMPLEX

        # measure text size
        (w, h), baseline = cv2.getTextSize(label, font, font_scale, thickness)

        # draw box
        cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)

        # draw filled bg for text
        cv2.rectangle(
            img,
            (x1, y1 - h - 2*pad),
            (x1 + w + 2*pad, y1),
            color,
            thickness=-1
        )
        # draw the label in white
        cv2.putText(
            img,
            label,
            (x1 + pad, y1 - pad),
            font,
            font_scale,
            (255, 255, 255),
            thickness,
            cv2.LINE_AA
        )


    return img
