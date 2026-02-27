# Waters MVP - Main Application File
    # Backend Logic - Handles core functionality & data processing for Waters MVP

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
import uvicorn
import os
import uuid
import json

app = FastAPI(title="Water Snap & Map API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React (Vite)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Models (like InventoryItem)
# -------------------------

class IdentifyResponse(BaseModel):
    suggestions: list[str]
    fact: str


class UserStats(BaseModel):
    user_id: str
    uses: int


# -------------------------
# Temporary in-memory storage
# -------------------------

user_usage = {}

# Define the data model for uploaded images
class UploadedImage(BaseModel):
    file_name: str
    description: str

# Temporary in-memory storage for uploaded images
uploaded_images = []

UPLOAD_DIR = "uploads"  # Ensure this directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------------
# Helper Functions
# -------------------------

def get_user_uses(user_id: str) -> int:
    return user_usage.get(user_id, 0)

def increment_user_uses(user_id: str) -> int:
    user_usage[user_id] = get_user_uses(user_id) + 1
    return user_usage[user_id]

def build_prompt(uses: int) -> str:
    if uses <= 2:
        guidance = "User is new. Keep suggestions more general if uncertain."
    else:
        guidance = "User is returning. Be more specific when possible."

    return f"""
You are a nature guide that knows about water, wetlands, animals, and plants. 

Find ONE organism in the image.

1) Find ONE organism in the image. Provide 1-3 suggestions.
   - If uncertain, include 'unknown species' as the LAST option.
   - {guidance}

2) Provide EXACTLY 1 interesting fact.
   - 10-second read for a 5th grader.
   - Focus on wetlands ecology.

Return ONLY valid JSON:
{{
  "suggestions": ["...", "...", "..."],
  "fact": "..."
}}
"""
        # "You are a nature guide that knows about water, wetlands, and ecologically important and visible life. "
        # "Focus on organisms that are visible without a magnifying glass. "
        # "Animals include birds, mammals, reptiles, amphibians, fish, and insects. "
        # "Plants include trees, flowers, shrubs, grasses, and moss. "
        # "Include other ecologically important and visible life, such as algae and fungi. "
        # "Your goal is to teach about ecologically important wetlands organisms, which are visible without a magnifying glass. "
        # "Assume learners have a 10-second attention span. "
        # "You do not encourage observers to get closer or evaluate the wetland environment. "
        # "Instead, process one image and text prompt using the LLaMA Vision model. "
        # "First, describe the image and provide common names—not genus and species. "
        # "If species is unclear, suggest higher taxonomic levels (e.g., Genus, Family). "
        # "At the roughest level, suggestions should be 'plant', 'animal', or 'unknown species'. "
        # "Second, provide 1 interesting fact related to the taxonomic recommendations that would take a 5th grader about 10 seconds to read. "
        # "The fact should be concise, engaging, and focused on wetlands plants and animals, fresh water, and the ecological importance of wetlands. "
        # "What is in this image?"

def parse_model_response(response):
    try:
        content = response["message"]["content"]
        data = json.loads(content)
        return data["suggestions"], data["fact"]
    except Exception:
        # fallback if model formatting breaks
        return ["unknown species", "unknown species", "unknown species"], str(response)


# -------------------------
# Routes (structured like your inventory example)
# -------------------------

@app.get("/api/health")
def health():
    return {"status": "ok"}

# Users who are registered to track usage, but no authentication for simplicity
@app.get("/api/users/{user_id}")
def get_user(user_id: str):
    return UserStats(user_id=user_id, uses=get_user_uses(user_id))

# PROXIMATE GOAL: Main endpoint for identifying organisms or water characteristics in images of water and wetlands. 
    # User uploads image, and we return suggestions and an interesting fact.
@app.post("/api/identify", response_model=IdentifyResponse)
async def identify(user_id: str, image: UploadFile = File(...)):

    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    # Save temporary file
    original_name = image.filename or "upload.jpg"
    ext = os.path.splitext(original_name)[1] or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    contents = await image.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    # Track usage
    uses = increment_user_uses(user_id)

    # Call Ollama vision model
    try:
        response = ollama.chat(
            model="llama3.2-vision",
            messages=[{
                "role": "user",
                "content": build_prompt(uses),
                "images": [file_path],
            }]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Optional cleanup
        try:
            os.remove(file_path)
        except:
            pass

    suggestions, fact = parse_model_response(response)

    return IdentifyResponse(
        suggestions=suggestions,
        fact=fact
    )

# POST endpoint to handle image uploads
# This is a critical function that connects the frontend's upload button to the backend logic
@app.post("/api/images", status_code=201)
def upload_image(file: UploadFile, description: str):
    if not file.content_type.startswith("image/"):
        # Validate that the uploaded file is an image
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    # Save the uploaded file to the server
    file_extension = os.path.splitext(file.filename)[1]  # Extract file extension
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"  # Generate a unique filename
    file_path = os.path.join(UPLOAD_DIR, unique_filename)  # Full path for saving the file

    with open(file_path, "wb") as f:
        f.write(file.file.read())  # Write the file content to the server

    # Add metadata to in-memory storage
    new_image = {
        "file_name": unique_filename,  # Store the unique filename
        "description": description  # Store the user-provided description
    }
    uploaded_images.append(new_image)  # Append the metadata to the in-memory list
    return new_image  # Return the metadata as the response

# GET: List all uploaded images
@app.get("/api/images")
def get_uploaded_images():
    return uploaded_images  # Return the list of uploaded images

# DELETE: Delete an uploaded image by file name
@app.delete("/api/images/{file_name}")
def delete_uploaded_image(file_name: str):
    for i, image in enumerate(uploaded_images):
        if image["file_name"] == file_name:
            removed_image = uploaded_images.pop(i)  # Remove the image metadata from the list
            # Remove the file from the server
            file_path = os.path.join(UPLOAD_DIR, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)  # Delete the file from the server
            return {"deleted": True, "file_name": removed_image["file_name"]}  # Return confirmation
    raise HTTPException(status_code=404, detail="Image not found")  # Raise error if file not found

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

