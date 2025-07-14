from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.detector import detect_objects
from app.sms import send_sms_termii

import numpy as np
import cv2
from io import BytesIO


app = FastAPI()

# CORS (for testing from other origins like mobile)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Farm Threat Detection API!"}

@app.post("/detect")
async def detect(file: UploadFile = File(...),  
                 phone_number: str = Form(...),
                 ):
    # Read image bytes
    image_bytes = await file.read()
    np_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    # Detect using YOLOv8
    detections = detect_objects(image)

    if detections:
        # Prepare SMS message
        labels = [d["label"] for d in detections]
        message = f"Alert from Yolo: {', '.join(labels)} detected on your farm."

        # Send SMS using Termii
        send_sms_termii(phone_number, message)

    return {"threats": detections}
