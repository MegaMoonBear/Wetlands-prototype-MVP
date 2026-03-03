# Unit tests for identify() - These tests mock external ollama.chat() API to ensure...
# fast, reliable, and isolated testing without making real model calls. The suite verifies:
# 1) Expected behavior under normal conditions (happy path),
# 2) Proper handling of edge outputs like "unknown species",
# 3) Robust error handling when the API raises exceptions.
# 4) "Helper class" to simulate file uploads.
# The goal is to test behavior and response structure—not the external model itself.

import pytest
from unittest.mock import patch  # Used to mock external dependencies
from main import identify, build_prompt, parse_model_response  # Import updated methods from main.py
from fastapi import HTTPException  # Exception handling for FastAPI
from fastapi.datastructures import UploadFile  # Base class for file uploads in FastAPI
from io import BytesIO  # Used to simulate file content in memory

# ------------------------
# HAPPY PATH TEST
# ------------------------
@patch("main.ollama.chat")  # Mocking the ollama.chat function
async def test_identify_success(mock_chat):
    # Mocking the response from the Ollama Vision model
    mock_chat.return_value = {
        "message": {
            "content": "{\"suggestions\": [\"animal\"], \"fact\": \"This bird can see ultraviolet light.\"}"
        }
    }

    # Simulating the identify function with a fake file upload
    response = await identify("user123", image=FakeUploadFile())

    # Assertions to verify the response structure and content
    assert response.suggestions == ["animal"]  # Verifies the suggestions list
    assert response.fact == "This bird can see ultraviolet light."  # Verifies the fact string
    mock_chat.assert_called_once()  # Ensures the mock was called exactly once

# ------------------------
# EDGE CASE TEST
# ------------------------
@patch("main.ollama.chat")  # Mocking the ollama.chat function
async def test_identify_unknown_species(mock_chat):
    # Mocking the response for an unknown species case
    mock_chat.return_value = {
        "message": {
            "content": "{\"suggestions\": [\"unknown species\"], \"fact\": \"Some organisms are hard to identify.\"}"
        }
    }

    # Simulating the identify function with a fake file upload
    response = await identify("user123", image=FakeUploadFile())

    # Assertions to verify the response structure and content
    assert "unknown species" in response.suggestions  # Verifies the presence of "unknown species"
    assert response.fact == "Some organisms are hard to identify."  # Verifies the fact string

# ------------------------
# ERROR HANDLING TEST
# ------------------------
@patch("main.ollama.chat")  # Mocking the ollama.chat function
async def test_identify_api_failure(mock_chat):
    # Simulating an API failure by raising an exception
    mock_chat.side_effect = Exception("API failure")

    # Verifying that the identify function raises an HTTPException
    with pytest.raises(HTTPException) as exc_info:
        await identify("user123", image=FakeUploadFile())

    # Assertions to verify the exception message
    assert "API failure" in str(exc_info.value)  # Verifies the exception message

# ------------------------
# Helper class to simulate file upload 
    # The FakeUploadFile helper class simulates file uploads, so tests have controlled and reusable input 
    # It abstracts file handling so tests can focus on behavior (not upload mechanics)
# ------------------------
class FakeUploadFile(UploadFile):
    # The FakeUploadFile helper class simulates file uploads, so tests have controlled and reusable input 
    # It abstracts file handling so tests can focus on behavior (not upload mechanics)
    def __init__(self):
        # Simulating a file with a name and content type
        super().__init__(filename="fake_image.jpg", file=BytesIO(b"fake image content"))  # BytesIO simulates file content in memory
        self.content_type = "image/jpeg"  # Setting a valid content type for the simulated image file
