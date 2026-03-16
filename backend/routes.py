# This file defines API endpoints for the backend service.
# upload → save → validate → extract metadata → analyze image → store → respond

from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from services.exif_metadata import extract_exif_metadata
from db_utils import insert_exif_metadata
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

# Define maximum file size (5 MB)
MAX_FILE_SIZE = 5 * 1024 * 1024


# Request model (matches frontend payload)
class ImageUploadRequest(BaseModel):
    filename: str
    image: str   # base64 string


@router.post("/upload-image")
async def upload_image(payload: ImageUploadRequest):
    """
    Endpoint for image uploads sent as Base64 JSON.
    Extracts EXIF metadata, runs AI analysis, and returns results.
    """

    media_id = str(uuid.uuid4())
    temp_filename = f"{media_id}_{payload.filename}"
    file_location = os.path.join(TMP_DIR, temp_filename)

    try:
        # Decode base64 image
        image_bytes = base64.b64decode(payload.image)

        if len(image_bytes) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File size exceeds the 5 MB limit.")

        # Save temporary file
        with open(file_location, "wb") as buffer:
            buffer.write(image_bytes)

    except Exception as decode_error:
        raise HTTPException(status_code=400, detail=f"Invalid Base64 image data: {decode_error}")

    try:
        # Extract EXIF metadata
        metadata = extract_exif_metadata(file_location)

        if metadata:
            insert_exif_metadata(media_id, metadata)

    except Exception as exif_error:
        raise HTTPException(status_code=500, detail=f"EXIF extraction error: {exif_error}")

    try:
        # Run AI image analysis
        ai_response = analyze_wetland_image(file_location)

    except Exception as ai_error:
        raise HTTPException(status_code=500, detail=f"AI processing error: {ai_error}")

    try:
        # Move file to permanent storage
        permanent_storage_path = os.path.join(UPLOAD_DIR, temp_filename)
        shutil.move(file_location, permanent_storage_path)

    except Exception as move_error:
        raise HTTPException(status_code=500, detail=f"Error moving the file to permanent storage: {move_error}")

    return JSONResponse(
        content={
            "message": "AI analysis completed successfully",
            "media_id": media_id,
            "metadata": metadata,
            "ai_response": ai_response
        }
    )