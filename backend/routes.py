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
from services.exif_metadata import extract_exif_metadata  # Updated import to resolve circular dependency
from db_utils import insert_exif_metadata  # Import the database insertion function
from ollama_vision import analyze_wetland_image # Import function to analyze images with ollama
import os
import shutil  # For moving files
import tempfile  # For creating temporary files


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

     # Validate file format - only allow common image formats (e.g., JPG, PNG) 
     # to ensure compatibility with AI model and prevent processing errors.
    try:
        if not file.filename or not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a JPG, JPEG, or PNG file.")
    except HTTPException as format_error:
        return JSONResponse(content={"error": format_error.detail}, status_code=format_error.status_code)

    try:
        file_size = int(request.headers.get("content-length", 0))  # Get file size from request headers
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File size exceeds the 5 MB limit.")
    except HTTPException as size_error:
        return JSONResponse(content={"error": size_error.detail}, status_code=size_error.status_code)

    try:
        temp_dir = tempfile.gettempdir()  # Get the system's temporary directory
        file_location = f"{temp_dir}/{file.filename}"  # Define temporary file path
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())  # Write the uploaded file to the temporary location
    except Exception as file_error:
        raise HTTPException(status_code=500, detail=f"Error saving the file: {file_error}")
    finally:
        if file_location and os.path.exists(file_location):
            os.remove(file_location)  # Ensure temporary file is deleted

    try:
        # Placeholder for AI model integration
        analysis = analyze_wetland_image(file_location)
        print(analysis)



        # Use analyze_wetland_image from ollama_vision.py file here



    except Exception as ai_error:
        raise HTTPException(status_code=500, detail=f"AI processing error: {ai_error}")

    try:
        permanent_storage_path = f"uploads/{file.filename}"
        shutil.move(file_location, permanent_storage_path)  # Move the file to the uploads/ directory
    except Exception as move_error:
        raise HTTPException(status_code=500, detail=f"Error moving the file to permanent storage: {move_error}")

    try:
        # Example: Insert into media table (replace with actual DB logic)
        # insert_media_to_db(media_id, observation_id, permanent_storage_path)
        pass

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
