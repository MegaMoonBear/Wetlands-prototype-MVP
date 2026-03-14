# Water MVP - Main Application File
    # Backend Logic - Handles core functionality & data processing (inclu. image) for water MVP

from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from collections import defaultdict  # Simplifies user usage tracking
import ollama
import uvicorn
import os
from dotenv import load_dotenv
from pathlib import Path  # Modern file handling
import uuid
import json
import routes 
from PIL import Image
from PIL.ExifTags import TAGS

# ---------------------------------------------------------
# FastAPI app initialization
    # variable 'app' represents your fast api app - should be in this main.py file and 
    # next 3 "app" are good use of FastAPI's features, such as: 
        # dependency injection for DB sessions and 
        # CORS middleware for frontend integration
# ---------------------------------------------------------
app = FastAPI(title="Water Snap & Map API")

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React (Vite)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)  # Include routes from the routes.py file (modularizes route definitions)

# ---------------------------------------------------------
# Environment Variables for API and Database Configuration
# ---------------------------------------------------------
load_dotenv()  # Load environment variables from .env file
# api_key = os.getenv("OLLAMA_API_KEY")  # Not needed for local Ollama ((Load Ollama API key from environment variable
DB_PORT = os.getenv("DB_PORT")  # Load database port from environment variable
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Load database password from env. vari.

# ---------------------------------------------------------
# Database connection (Neon/PostgreSQL)
# ---------------------------------------------------------
DATABASE_URL ="postgresql+asyncpg://postgres:@localhost:5432/postgres"
engine = create_async_engine(DATABASE_URL, echo=False)
# creating a session factory using SQLAlchemy's sessionmaker
    # sessionmaker is a function used to configure and generate new database session objects
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
# ASL later used in get_session dependency to provide database sessions for FastAPI routes.
# Without this line, no sessions, so any route that interacts with the database would fail.

# ---------------------------------------------------------
# Pydantic models for validation
# ---------------------------------------------------------
class FeedbackIn(BaseModel):
    topic: str
    details: str

class IdentifyResponse(BaseModel):
    suggestions: list[str]
    fact: str

class UserStats(BaseModel):
    user_id: str
    uses: int

# ---------------------------------------------------------
# Dependency to get DB session
# ---------------------------------------------------------
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

# ---------------------------------------------------------
# Temporary in-memory storage
# ---------------------------------------------------------
user_usage = defaultdict(int)  # Simplified user usage tracking
uploaded_images = []  # Temporary storage for uploaded images
UPLOAD_DIR = Path("uploads")  # Using pathlib for file handling
UPLOAD_DIR.mkdir(exist_ok=True)  # Ensure the directory exists

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def increment_user_uses(user_id: str) -> int:
    user_usage[user_id] += 1  # Simplified with defaultdict
    return user_usage[user_id]

# ---------------------------------------------------------
# Prompt construction for image processing
# ---------------------------------------------------------
# **SUGGESTION - NEXT LINES: Provide image processing guidance as separate lines .**
# **WHY: Improve readability and clarity, especially without Word Wrap and for long prompts.**
def build_prompt(uses: int) -> str:
    guidance = "User is new. Keep suggestions more general if uncertain." if uses <= 2 else "User is returning. Be more specific when possible."
    return f"""
You are a nature guide that knows about water, wetlands, animals, plants, and other living organisms. 
Animals include all lliving, except plants - insects, amphibians, fish, etc. 
Plants include all living except animals - trees, shrubs, grasses, flowers, etc. 
Other living organisms include fungi, algae, bacteria, etc.

1) Find ONE living or dead organism in the image. 
   - If none present, go to second step and provide fact. 
   - If uncertain, include 'unknown species' as the LAST option.
   - {guidance}

2) Provide EXACTLY 1 interesting fact.
   - 10-second read for a 5th grader.
   - Focus on wetlands ecology.

   
Return ONLY valid JSON:
{{
  "fact": "..."
}}
"""
#   "suggestions": ["...", "...", "..."],
# **SUGGESTION - PRIOR LINES: Provide image processing guidance as separate lines .**
# **WHY: Improve readability and clarity, especially without Word Wrap and for long prompts.**


def parse_model_response(response):
    try:
        content = response["message"]["content"]
        data = json.loads(content)
        return data["suggestions"], data["fact"]
    except Exception:
        return ["unknown species"] * 3, str(response)  # Fallback for invalid responses



# ---------------------------------------------------------
# Image processing and EXIF metadata extraction
# ---------------------------------------------------------
def extract_exif_metadata(image_path):
    """
    Extracts EXIF data from an image using Pillow and returns a dictionary.
        Code extract_exif_metadata to provide data for insert_exif_metadata in db_utils.py
        Verify workflow - Confirm that extract_exif_metadata outputs data structure to fit insert_exif_metadata
    """
    exif_data = {}
    try:
        image = Image.open(image_path)
        # Verify image is a valid EXIF image
        image.verify() 
        info = image.getexif()
        if info:
            for tag, value in info.items():
                decoded_tag = TAGS.get(tag, tag)
                exif_data[decoded_tag] = value
    except (IOError, FileNotFoundError, AttributeError):
        print(f"Error processing image: {image_path}")
        pass
    return exif_data


# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------
@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/users/{user_id}")
def get_user(user_id: str):
    return UserStats(user_id=user_id, uses=user_usage[user_id])

# AI SUGGESTION: Consolidate image handling logic into a utility function.
# AI REASONING: Avoid redundancy in /api/identify and other routes that process images.
# This function needs to be adjusted for image processing by the AI model - not "str"
@app.post("/api/identify", response_model=IdentifyResponse)
async def identify(user_id: str, image: UploadFile = File(...)):
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    # Ensure image.filename is not None before using it
    if not image.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a filename and that name must be valid.")

    file_path = UPLOAD_DIR / f"{uuid.uuid4().hex}{Path(image.filename).suffix}"
    with file_path.open("wb") as f:
        f.write(await image.read())

    increment_user_uses(user_id)

    try:
        response = ollama.chat(
            model="llama3.2-vision",
            messages=[{
                "role": "user",
                "content": build_prompt(user_usage[user_id]),
                "images": [str(file_path)],
            }]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file_path.unlink(missing_ok=True)  # Cleanup temporary file

    suggestions, fact = parse_model_response(response)
    return IdentifyResponse(suggestions=suggestions, fact=fact)

