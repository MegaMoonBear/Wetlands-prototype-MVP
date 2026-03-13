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

router = APIRouter(prefix="/upload", tags=["upload"])  # Create a router for upload-related endpoints

# extract_exif_metadata   # Placeholder function for EXIF extraction  
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


@router.post("/upload-image")
async def upload_image(request: Request,  file: UploadFile = File(...)):
    """
    Endpoint to handle image uploads, extract EXIF metadata, and store it in the database.

    Args:
        file (UploadFile): The uploaded image file.

    Returns:
        JSONResponse: A response containing the extracted EXIF metadata.
    """
    # Initialize file_location to an empty string outside the try block to ensure it is always defined
    file_location = ""

    try:
        # Validate file format
        if not file.filename or not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a JPG, JPEG, or PNG file.")

        # Check file size
        file_size = int(request.headers.get("content-length", 0))
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File size exceeds the 5 MB limit.")

        # Save the uploaded file temporarily
        try:
            file_location = f"/tmp/{file.filename}"
            with open(file_location, "wb") as buffer:
                buffer.write(await file.read())  # Write the uploaded file to a temporary location
        except Exception as file_error:
            raise HTTPException(status_code=500, detail=f"Error saving the file: {file_error}")

        # Validate that the file is a valid image
        try:
            exif_metadata = extract_exif_metadata(file_location)
        except Exception as exif_error:
            raise HTTPException(status_code=422, detail=f"Invalid image content or corrupted EXIF data: {exif_error}")

        # Handle missing or corrupted EXIF data
        if not exif_metadata:
            raise HTTPException(status_code=422, detail="No EXIF metadata found or the data is corrupted.")

        # Insert the extracted EXIF metadata into the database
        media_id = "example-media-id"  # Replace with the actual media ID from your workflow
        try:
            insert_exif_metadata(media_id, exif_metadata)  # Call the database insertion function
        except Exception as db_error:
            raise HTTPException(status_code=500, detail=f"Database error: {db_error}")

        # Return the extracted metadata as a JSON response
        return JSONResponse(content={"message": "Image uploaded and metadata stored successfully", "exif_metadata": exif_metadata})

    except HTTPException as http_exc:
        # Handle HTTP exceptions with appropriate status codes and messages
        return JSONResponse(content={"error": http_exc.detail}, status_code=http_exc.status_code)

    except Exception as e:
        # Handle any other unexpected errors
        return JSONResponse(content={"error": f"An unexpected error occurred: {e}"}, status_code=500)

    finally:
        # Clean up temporary files if file_location is not empty and the file exists
        if file_location and os.path.exists(file_location):
            os.remove(file_location)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)  # Run the FastAPI app on localhost