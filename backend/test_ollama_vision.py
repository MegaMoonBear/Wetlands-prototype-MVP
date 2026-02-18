# Unit tests for analyze_wetland_image() or __________ - These tests mock external ollama.chat() API to ensure...
# fast, reliable, # and isolated testing without making real model calls. The suite verifies:
    # 1) Expected behavior under normal conditions (happy path),
    # 2) Proper handling of edge outputs like "unknown species",
    # 3) Robust error handling when the API raises exceptions.
# The goal is to test behavior and response structure—not the external model itself.

import pytest
from unittest.mock import patch
from ollama_vision import analyze_wetland_image


# ------------------------
# HAPPY PATH TEST
# ------------------------
@patch("ollama.chat")
def test_analyze_wetland_image_success(mock_chat):
    mock_chat.return_value = {
        "message": {
            "content": "animal - This bird can see ultraviolet light."
        }
    }

    result = analyze_wetland_image("fake/path/image.jpg")

    assert result["message"]["content"].startswith("animal")
    mock_chat.assert_called_once()


# ------------------------
# EDGE CASE TEST
# ------------------------
@patch("ollama.chat")
def test_analyze_wetland_image_unknown_species(mock_chat):
    mock_chat.return_value = {
        "message": {
            "content": "unknown species - Some organisms are hard to identify."
        }
    }

    result = analyze_wetland_image("fake/path/image.jpg")

    assert "unknown species" in result["message"]["content"]


# ------------------------
# ERROR HANDLING TEST
# ------------------------
@patch("ollama.chat")
def test_analyze_wetland_image_api_failure(mock_chat):
    mock_chat.side_effect = Exception("API failure")

    with pytest.raises(Exception) as exc_info:
        analyze_wetland_image("fake/path/image.jpg")

    assert "API failure" in str(exc_info.value)
