# routes.py
# This file defines API endpoints for the backend service.
# Tasks:
# - Currently unused as the prototype does not include a frontend or API routes.
# - Future use: Define routes for interacting with sandbox modules.

# Example: Define routes for image uploads, data retrieval, and other functionalities. 
# Use a framework like Flask or FastAPI to create and manage routes.


# integrate EXIF extraction into the /upload-image endpoint, which: 
    # saves the uploaded image temporarily, 
    # extracts EXIF metadata using the extract_exif_metadata function, and 
    # returns the metadata as a JSON response. 

# FastAPI app setup
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from app import extract_exif_metadata  # Import the EXIF extraction function
from db_utils import insert_exif_metadata  # Import the database insertion function
import os

app = FastAPI()

# Define maximum file size (e.g., 5 MB)
MAX_FILE_SIZE = 5 * 1024 * 1024

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...), request: Request):
    """
    Endpoint to handle image uploads, extract EXIF metadata, and store it in the database.

    Args:
        file (UploadFile): The uploaded image file.

    Returns:
        JSONResponse: A response containing the extracted EXIF metadata.
    """
    try:
        # Validate file format
        if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a JPG, JPEG, or PNG file.")

        # Check file size
        file_size = int(request.headers.get("content-length", 0))
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File size exceeds the 5 MB limit.")

        # Save the uploaded file temporarily
        file_location = f"/tmp/{file.filename}"
        try:
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
        # Clean up temporary files
        if os.path.exists(file_location):
            os.remove(file_location)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run the FastAPI app on localhost