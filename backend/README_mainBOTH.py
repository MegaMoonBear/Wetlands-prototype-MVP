# Wetlands MVP - Main Application File
    # Backend Logic - Handles core functionality & data processing for Wetlands MVP

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import ollama
import uvicorn
import os
import uuid
import json

app = FastAPI(title="Wetlands Snap & Map API")

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

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "tmp_uploads")
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
You are a nature guide that knows about animals and plants.

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
        # "You are a nature guide that knows about water, wetlands, animals, and plants. "
        # "Animals include birds, mammals, reptiles, amphibians, fish, and insects. "
        # "Plants include trees, flowers, shrubs, grasses, and fungi. "
        # "Your goal is to teach about wetlands plants and animals, assuming learners have a 10-second attention span. "
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


@app.get("/api/users/{user_id}")
def get_user(user_id: str):
    return UserStats(user_id=user_id, uses=get_user_uses(user_id))


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


# -------------------------
# Run server
# -------------------------

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)



# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse

# # Import  for image processing
# import ollama
# import uvicorn

# # from PIL import Image, ExifTags

# app = FastAPI()

# # Adapted from Model_RAG_response.py for integration into the main application workflow
# def main():
#     # Entry point for the application
#     print("Welcome to the Water Snap and Map pilot")

#     # Placeholder: Simulate user uploading an image
#     print("Simulating user uploading an image...")
#     user_uploaded_image = "C:\\Users\\Meghan Carr\\Desktop\\Meghan - ALL til OneDrive\\5-0 - Portfolio Projects\\Wetland\\Water prototype\\Wetlands-prototype-MVP\\backend\\sandbox\\images\\Iris_Pinks_Orange_Burg.jpg"  # Replaced with actual file path in temporary image folder

#     # Placeholder: Process the uploaded image using Model_RAG_response
#         # utilize the ollama.chat method, which is imported from Model_RAG_response.py
#     print("Processing the uploaded image using LLaMA Vision model...")
#     response = ollama.chat(         # ollama is imported from Model_RAG_response.py
#         model='llama3.2-vision',  # Specify the model to use for image processing
#         messages=[{                 # same structure as in Model_RAG_response.py
#             'role': 'user',  # Define the role of the message sender
#             'content': "You are nature guide that knows about animals and plants. Animals include birds, mammals, reptiles, amphibians, fish, and insects. Plants include trees, flowers, shrubs, grasses, and fungi. Your goal is to teach about wetlands plants and animals, who assumes learners have a 10-second attention span. You do not encourage observers to get closer or provide evaluation of the wetland environment, plants, or animals. Instead, process one image and text prompt using the LLaMA Vision model. Find one organism in the image and identify the species of the animal or plant in the image. First, provide 3 suggestions for the single plant or animal. Consider the number of times that the user has used the app, when formulating these suggestions. Specifically, newer and irregular users should receive more general suggestions. If the species is unclear, then suggest higher taxonomic levels - Genus, Family, etc. At the roughest level, suggestions should be 'plant', 'animal', or 'unknown species'. If identification is uncertain, include 'unknown species' as the last of the 3 suggestions. Second, provide 1 interesting fact related to the taxonomic recommendations that would take a 5th grader about 10 seconds to read. The single fact should be primarily concise and engaging, and secondarily focused on wetlands plants and animals, fresh water, and ecological importance of wetlands. Draw upon reliable nature guide knowledge. What is in this image?",  # Providing prompt for model 
#             'images': [user_uploaded_image]  # Eventually will attach user-uploaded image for processing
#         }]
#     )

#     # Function to extract EXIF metadata from an image file
# # def extract_exif_metadata(file_path):
# #     """
# #     Extract EXIF metadata from an image file.

# #     Args:
# #         file_path (str): Path to the image file.

# #     Returns:
# #         dict: A dictionary containing EXIF metadata.
# #     """
# #     try:
# #         # Open the image file using Pillow
# #         image = Image.open(file_path)

# #         # Retrieve EXIF data from the image (if available)
# #         exif_data = image.getexif()

# #         if not exif_data:
# #             # Return an empty dictionary if no EXIF data is found
# #             return {}

# #         # Map EXIF tags to human-readable names using ExifTags.TAGS
# #         exif_metadata = {
# #             ExifTags.TAGS.get(tag, tag): value  # Use tag name if available, else use tag ID
# #             for tag, value in exif_data.items()
# #             if tag in ExifTags.TAGS  # Filter only known EXIF tags
# #         }

# #         return exif_metadata

# #     except Exception as e:
# #         # Handle errors gracefully and print the error message
# #         print(f"Error extracting EXIF metadata: {e}")
# #         return {}

#     # Placeholder: Display the response
#     print("Response from LLaMA Vision model:")
#     print(response)  # Output the model's response to the console

# if __name__ == "__main__":
    
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)  # Start the FastAPI server

#     # Replace 'example.jpg' with the path to your image file
#     file_path = "example.jpg"                                   ##############################POST REQUEST, REPLACE WITH USER-UPLOADED IMAGE PATH IN TEMPORARY IMAGE FOLDER

#     # # Call the function to extract EXIF metadata
#     # metadata = extract_exif_metadata(file_path)

#     # # Print the extracted metadata to the console
#     # print("Extracted EXIF Metadata:", metadata)

