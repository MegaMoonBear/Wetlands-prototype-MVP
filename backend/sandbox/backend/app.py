# app.py
# This file serves as the entry point for the backend server.
# Tasks:
# - Orchestrate the workflow between sandbox modules.
# - Call functions from sandbox/image_loader.py to load and preprocess images.
# - Call sandbox/llama_service.py to send images to the AI model.
# - Call sandbox/response_handler.py to process the AI's response.
# - Call sandbox/database_saver.py to save results to the database.
# - Call sandbox/console_output.py to display results in the console.

# Use a framework like Flask or FastAPI to define routes and handle requests.
# Example: Define API endpoints to interact with the frontend and database.
# Ensure proper error handling and logging for debugging.


# app.py: If app.py is the entry point for the backend, it might need updates to include routes or endpoints that utilize the Llama 3.2-Vision functionality.

# central location for integrating EXIF extraction into the media upload workflow
# Library Recommendation: Use Pillow for EXIF data extraction, because:
    # versatile, actively maintained, and integrates well with other image processing tasks.

from PIL import Image, ExifTags

# Function to extract EXIF metadata from an image file
def extract_exif_metadata(file_path):
    """
    Extract EXIF metadata from an image file.

    Args:
        file_path (str): Path to the image file.

    Returns:
        dict: A dictionary containing EXIF metadata.
    """
    try:
        # Open the image file using Pillow
        image = Image.open(file_path)

        # Retrieve EXIF data from the image (if available)
        exif_data = image._getexif()

        if not exif_data:
            # Return an empty dictionary if no EXIF data is found
            return {}

        # Map EXIF tags to human-readable names using ExifTags.TAGS
        exif_metadata = {
            ExifTags.TAGS.get(tag, tag): value  # Use tag name if available, else use tag ID
            for tag, value in exif_data.items()
            if tag in ExifTags.TAGS  # Filter only known EXIF tags
        }

        return exif_metadata

    except Exception as e:
        # Handle errors gracefully and print the error message
        print(f"Error extracting EXIF metadata: {e}")
        return {}

# Example usage block for testing the function - flasked out when imported as a module
if __name__ == "__main__":
    # Replace 'example.jpg' with the path to your image file
    file_path = "example.jpg"

    # Call the function to extract EXIF metadata
    metadata = extract_exif_metadata(file_path)

    # Print the extracted metadata to the console
    print("Extracted EXIF Metadata:", metadata)
