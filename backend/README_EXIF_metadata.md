## EXIF for Metadata Extraction ##
**Recommendation: Use EXIF for Metadata Extraction**
For a novice coder, EXIF (Exchangeable Image File Format) is recommended over IPTC (International Press Telecommunications Council) for the following reasons:

## Pros of EXIF ## 
Widespread Support:

EXIF metadata is embedded in most modern image formats (e.g., JPEG, TIFF) and is widely supported by libraries like Pillow (Python Imaging Library) and exifread.
Easier to access and manipulate for beginners.
Rich Metadata:

EXIF provides detailed metadata, including date-time, camera settings, GPS coordinates, and more, which are directly relevant to your app's pilot phase.
Ease of Use:

Libraries like Pillow make it straightforward to extract EXIF data with minimal setup.
Relevance to Your App:

EXIF includes GPS data (latitude and longitude), which aligns with your app's need to associate observations with locations.

## Cons of EXIF ## 
Limited Editing:
EXIF metadata is primarily read-only for most use cases. Editing EXIF data requires additional tools or libraries.
Not All Images Have EXIF:
Some images (e.g., screenshots, edited images) may lack EXIF metadata.

## Pros of IPTC ## 
Standard for Professional Media:
IPTC metadata is widely used in journalism and media industries for tagging and categorizing images.
Custom Metadata:
IPTC allows for more customizable fields, such as keywords, captions, and copyright information.
## Cons of IPTC ## 
Less Common in Consumer Images:
IPTC metadata is less common in images captured by consumer devices (e.g., smartphones, cameras).
Complexity:
Extracting IPTC metadata requires more advanced libraries (e.g., pyexiv2), which may be harder for a novice coder to use.

## Additional Services for the Pilot Phase ## 
EXIF:
Provides GPS data for associating observations with locations.
Includes date-time information for timestamping observations.
IPTC:
Useful for adding custom tags or descriptions to images, which could be helpful for categorizing observations in later phases.


## Database Table Setup for Metadata ## 
Your proposed database schema aligns well with the app's requirements. Here's how the tables can be structured to support metadata:

## Observation Table ## 

Attributes:
observation_ID (Primary Key)
date_time (EXIF metadata for timestamp)
source (e.g., user, device, or app version)
Purpose:
Tracks the overall observation event.

## Media Table ## 

Attributes:
media_ID (Primary Key)
observation_ID (Foreign Key to Observation Table)
metadata_extracted (JSON or text field for storing EXIF/IPTC metadata)
storage_URL (URL or path to the stored image)
Purpose:
Links media files to observations and stores extracted metadata.

## Location Table ## 

Attributes:
location_ID (Primary Key)
latitude (EXIF GPS metadata)
longitude (EXIF GPS metadata)
Purpose:
Stores location data for observations.

## Final Recommendation ## 
Use EXIF for metadata extraction during the pilot phase due to its simplicity and relevance.
Set up the database tables as described to store and manage metadata effectively.
Consider IPTC for future phases if you need custom tagging or categorization features.
