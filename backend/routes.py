# routes.py

from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ollama_vision import analyze_wetland_image

import uuid
import os
import shutil
import base64

router = APIRouter(prefix="/upload", tags=["upload"])

# Define directories
TMP_DIR = "tmp_uploads"
UPLOAD_DIR = "uploads"

os.makedirs(TMP_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILE_SIZE = 5 * 1024 * 1024


class ImageUploadRequest(BaseModel):
    filename: str
    image: str  # base64 string


@router.post("/upload-image")
async def upload_image(payload: ImageUploadRequest):

    media_id = str(uuid.uuid4())
    temp_filename = f"{media_id}_{payload.filename}"
    file_location = os.path.join(TMP_DIR, temp_filename)

    try:
        # Decode base64
        image_bytes = base64.b64decode(payload.image)

        if len(image_bytes) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")

        # Save temp file
        with open(file_location, "wb") as buffer:
            buffer.write(image_bytes)

    except Exception as decode_error:
        raise HTTPException(status_code=400, detail=f"Invalid Base64 data: {decode_error}")

    try:
        # AI analysis (uses file path now)
        ai_response = analyze_wetland_image(file_location)

    except Exception as ai_error:
        raise HTTPException(status_code=500, detail=f"AI processing error: {ai_error}")

    try:
        # Move file to permanent storage
        permanent_storage_path = os.path.join(UPLOAD_DIR, temp_filename)
        shutil.move(file_location, permanent_storage_path)

    except Exception as move_error:
        raise HTTPException(status_code=500, detail=f"File save error: {move_error}")

    return JSONResponse(
        content={
            "message": "AI analysis completed successfully",
            "media_id": media_id,
            "ai_response": ai_response
        }
    )