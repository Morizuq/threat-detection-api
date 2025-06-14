from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.detector import detect_objects
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

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    # Read image bytes
    image_bytes = await file.read()
    np_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    # Detect using YOLOv8
    detections = detect_objects(image)

    return {"threats": detections}
