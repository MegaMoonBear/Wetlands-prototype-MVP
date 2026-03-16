"""High-level interface to the Ollama Vision model.

This module exposes `analyze_wetland_image(image_path)` for programmatic
use. It is safe to import (no IO or network calls at import time).
"""

import logging
from typing import Dict, Optional
from ai_prompts import LLAMA_VISION_PROMPT
# Ollama client library used to call the LLaMA Vision model
import ollama
# Local utility to convert image files to base64; safe to import (no IO at import-time)
from image_util import convert_image_to_base64

logger = logging.getLogger(__name__)


def analyze_wetland_image(image_path: str) -> Dict:
    """Convert an image to base64 (when available) and call the Ollama Vision model.

        - If the image is missing or unreadable we log and call the model without
      `ollama.chat` without the image so tests can mock the model call.
    - Exceptions raised by `ollama.chat` are propagated so callers/tests can
      assert on them.
    """
    base64_image: Optional[str] = None
    try:
        base64_image = convert_image_to_base64(image_path)
    except FileNotFoundError:
        logger.warning("Image file not found: %s. Calling model without image.", image_path)
    except OSError as e:
        logger.warning("OS error reading image %s: %s. Calling model without image.", image_path, e)

    prompt = LLAMA_VISION_PROMPT

    message = {"role": "user", "content": prompt}
    if base64_image:
        message["images"] = [base64_image]

        # Uncomment the following lines after database creation to save the base64 string
        # with open("encoded_image.txt", "w") as f:
        #     f.write(base64_image)

    # Call the Ollama API; propagate exceptions to let callers/tests handle them
    response = ollama.chat(model="llama3.2-vision", messages=[message])
    return response
