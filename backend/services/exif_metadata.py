from PIL import Image
from PIL.ExifTags import TAGS

# ---------------------------------------------------------
# Image processing and EXIF metadata extraction 
     # ****MOVED from main.py to avoid circular reference****
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


# """
#     Placeholder function to extract EXIF metadata from an image file.
#     Replace with actual implementation using a library like Pillow or ExifRead.
#
#     Args:
#         file_path (str): The path to the image file."""
def extract_metadata(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image.getexif()
        
        if not exif_data:
            print("No EXIF data found in the image.")
            return

        metadata = {}
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            metadata[tag_name] = value
        
        # Print the metadata
        for key, value in metadata.items():
            print(f"{key}: {value}")

    except IOError:
        print(f"Error opening image file: {image_path}")

# Replaced 'your_image.jpg' with the path to my backend's images's folder's flower pic file
extract_metadata(r'C:\Users\Meghan Carr\Desktop\Meghan - ALL til OneDrive\5-0 - Portfolio Projects\Wetland\Water prototype\Wetlands-prototype-MVP\backend\images\Iris_Pinks_Orange_Burg.jpg')