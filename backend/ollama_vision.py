# ollama_vision.py

import logging
import ollama

from ai_prompts import LLAMA_VISION_PROMPT

logger = logging.getLogger(__name__)


def analyze_wetland_image(image_path: str) -> str:
    """
    Send image to Ollama Vision model using file path.
    Returns the model's text response.
    """

    message = {
        "role": "user",
        "content": LLAMA_VISION_PROMPT,
        "images": [image_path]  # ✅ MUST be a list
    }

    try:
        response = ollama.chat(
            model="llama3.2-vision",
            messages=[message]
        )

        return response.get("message", {}).get("content", "")

    except Exception as e:
        logger.error("Ollama error: %s", e)
        raise