# Wetlands-prototype-MVP

Clone the repository. Do not fork.
  
Cloning is the right move, since I: 
   
   - Started the repo yourself in GitHub
  
   - Will be coding locally in VS Code
  
   - Intend to push changes back to that same repo
  
Cloning:
  
   - Creates a local working copy on your machine
  
   - Keeps the repo connected to GitHub (origin)
  
   - Is the standard workflow for solo or primary-owner projects

# Minimum VS Code Setup (Day 3)

## Create a project folder

  Wetlands-prototype-MVP/
    ├── main.py
    ├── requirements.txt
    ├── images/
    │     └── sample_pond.jpg
    └── README.md

## Create and activate a virtual environment
  Keeps dependencies isolated
  
  Reviewers expect this

## Install dependencies
  LLaMA client library
  
  FastAPI (optional but helpful)
  
  Pillow or similar for image handling

## Confirm you can:
  Load a local image
  
  Print image metadata
  
  Make a simple API call

## DEPENDENCIES - What each dependency is doing (and why it belongs)
fastapi
  Why:
    Defines a simple backend API
    Cleanly structures endpoints
    Lightweight and modern
  Reviewer signal: You know how to scaffold backend logic without overengineering.

uvicorn
  Why:
    Runs FastAPI locally
    Zero configuration
    Industry standard ASGI server
  Reviewer signal: You understand how backends actually run.

python-multipart
  Why:
    Required for handling image uploads in FastAPI
    Even if you simulate uploads from local files, FastAPI expects this
  Reviewer signal: You didn’t “hack around” file handling.

pillow
  Why:
    Opens and validates image files
    Converts formats if needed
    Reads basic metadata
  Reviewer signal: You treat images as data, not blobs.

requests
  Why:
    Sends HTTP requests to the LLaMA Vision API
    Simple and widely trusted
  Reviewer signal: Clear, minimal API integration.

python-dotenv
  Why:
    Loads API keys from .env
    Keeps secrets out of code and GitHub
  Reviewer signal: You understand security basics
