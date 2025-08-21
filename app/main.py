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
import logging
from datetime import datetime

# Create timestamped log file
log_filename = f"logs_{datetime.now().strftime('%Y-%m-%d')}.log"

logging.basicConfig(
    filename=log_filename,
    filemode="a",  # append mode
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Welcome to the Farm Threat Detection API!"}

@app.post("/detect")
async def detect(file: UploadFile = File(...), phone_number: str = Form(...)):
    logger.info("📥 Request received")

    try:
        image_bytes = await file.read()
        np_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        logger.info("⚙️ Processing image")

        detections = detect_objects(image)

        if detections:
            labels = [d["label"] for d in detections]
            message = f"🚨 Alert from YOLO: {', '.join(labels)}"
            logger.info(f"✅ Threats detected: {labels}")
            send_sms_termii(phone_number, message)
        else:
            logger.info("✅ No threats detected.")

        return {"threats": detections}

    except Exception as e:
        logger.error(f"❌ Error during detection: {str(e)}")
        return {"error": "Internal Server Error"}
