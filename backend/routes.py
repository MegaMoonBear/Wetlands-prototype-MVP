# This file defines API endpoints for the backend service.
    # Example: Define routes for image uploads, data retrieval, and other functionalities. 
    # Use a framework like Flask or FastAPI to create and manage routes.

# integrate EXIF extraction into the /upload-image endpoint, which: 
    # saves the uploaded image temporarily (see "tmp_uploads" folder),
    # extracts EXIF metadata using the extract_exif_metadata function, and 
    # returns the metadata as a JSON response. 

# FastAPI app setup
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException, Request, APIRouter
from fastapi.responses import JSONResponse
# from app import extract_exif_metadata  # Import the EXIF extraction function
from db_utils import insert_exif_metadata  # Import the database insertion function
import os
from main import extract_exif_metadata  # Import the EXIF extraction function from main.py
from db_utils import insert_exif_metadata
from ai_prompts import LLAMA_VISION_PROMPT  # Import the AI prompt from the dedicated module
import shutil  # For moving files

router = APIRouter(prefix="/upload", tags=["upload"])  # Create a router for upload-related endpoints

# extract_exif_metadata - function for EXIF extraction of metadata for AI analysis 
    # Location, date/time, etc. that can provide context for AI analysis of water features and organisms
    # Those may also contribute to the AI's confidence in its analysis of the image
def process_image_route(image_path):
    """
    Placeholder function for a route that processes an image.
    """
    print(f"Processing image at path: {image_path}")

    # 1. Extract EXIF metadata
    metadata = extract_exif_metadata(image_path)
    print("Metadata extracted:", metadata)

    # 2. In this process_image_route function, define as unique identifier for media file
    media_id = str(uuid.uuid4())

    # 3. Insert metadata into the database
    if metadata:
        insert_exif_metadata(media_id, metadata)
        return "Metadata for image (media) file extracted and recorded."
    else:
        return "No EXIF metadata found or an error occurred."

# Example usage (you would replace this with actual route handling in a web app):
# if __name__ == "__main__":
#     # Assume 'sample_image.jpg' is in the same directory for this example
#     process_image_route("sample_image.jpg")
        
# Define maximum file size (e.g., 5 MB)
MAX_FILE_SIZE = 5 * 1024 * 1024

# backend contains a single POST route, /upload-image, which: 
    # handles image uploads, extracts EXIF metadata, and stores decomposed data in the database.
@router.post("/upload-image")
async def upload_image(request: Request, file: UploadFile = File(...)):
    """
    Endpoint for image uploads, extracting EXIF metadata, and returning an AI-generated response.

    Args:
        file (UploadFile): The uploaded image file.

    Returns:
        JSONResponse: A response containing the AI-generated analysis of the image.
    """
    file_location = ""  # Initialize file_location to ensure it is always defined
    permanent_storage_path = ""  # Path for storing the file permanently

    try:
        # Validate file format
        if not file.filename or not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a JPG, JPEG, or PNG file.")

        # Check file size
        file_size = int(request.headers.get("content-length", 0))  # Get file size from request headers
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File size exceeds the 5 MB limit.")

        # Save the uploaded file temporarily 
            # AI should analyze the temporary file in the /tmp directory before it is moved to the uploads/ directory. This ensures that:
            # file is validated and analyzed before being permanently stored
            # If an error occurs during AI analysis, file is not unnecessarily saved in permanent storage
        try:
            file_location = f"/tmp/{file.filename}"  # Define temporary file path
            with open(file_location, "wb") as buffer:
                buffer.write(await file.read())  # Write the uploaded file to the temporary location
        except Exception as file_error:
            raise HTTPException(status_code=500, detail=f"Error saving the file: {file_error}")

        # Perform AI analysis on temporary file
               # If AI analysis succeeds, file is moved to uploads/ directory for permanent storage.
        try:
            # Placeholder for AI model integration
            ai_response = {
                "prompt": LLAMA_VISION_PROMPT,  # Use the imported AI prompt
                "analysis": f"AI analysis for the image at {file_location}"  # Placeholder AI analysis
            }
        except Exception as ai_error:
            raise HTTPException(status_code=500, detail=f"AI processing error: {ai_error}")

        # Move the file to the permanent uploads/ directory
            # Ensures that the file is stored in a more permanent location after processing, and 
            # path can be saved in database for future reference.
        try:
            permanent_storage_path = f"uploads/{file.filename}"
            shutil.move(file_location, permanent_storage_path)  # Move the file to the uploads/ directory
        except Exception as move_error:
            raise HTTPException(status_code=500, detail=f"Error moving the file to permanent storage: {move_error}")

        # Save the file path in the database (placeholder for actual DB logic)
        try:
            # Example: Insert into media table (replace with actual DB logic)
            # insert_media_to_db(media_id, observation_id, permanent_storage_path)
            pass
        except Exception as db_error:
            raise HTTPException(status_code=500, detail=f"Database error: {db_error}")

        # Return the AI-generated response
        return JSONResponse(content={"message": "AI analysis completed successfully", "ai_response": ai_response})

    except HTTPException as http_exc:
        # Handle HTTP exceptions with appropriate status codes and messages
        return JSONResponse(content={"error": http_exc.detail}, status_code=http_exc.status_code)

    except Exception as e:
        # Handle any other unexpected errors
        return JSONResponse(content={"error": f"An unexpected error occurred: {e}"}, status_code=500)

    finally:
        if file_location and os.path.exists(file_location):  # Ensure temporary file is deleted
            os.remove(file_location)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)  # Run the FastAPI app on localhost