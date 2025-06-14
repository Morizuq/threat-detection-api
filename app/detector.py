from ultralytics import YOLO
import cv2
import numpy as np
from typing import List, Dict

# Load YOLOv8 model
model = YOLO("weights/yolov8n.pt") 

# Define threat classes
# THREAT_CLASSES = {"bird", "cow", "cat", "dog", "person"}
THREAT_CLASSES = {"bird", "cow", "cat", "dog"}

def detect_objects(image: np.ndarray) -> List[Dict]:
    results = model(image, imgsz=640)[0]
    
    detections = []
    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls_id]

       # Only keep threats with good confidence
        if label in THREAT_CLASSES and conf > 0.5:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            detections.append({
                "label": label,
                "confidence": round(conf, 2),
                "bbox": [x1, y1, x2, y2]
            })

    return detections
