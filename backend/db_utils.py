import psycopg2
from psycopg2.extras import Json

# Function to establish a connection to the PostgreSQL database
def get_db_connection():
    """
    Establish a connection to the PostgreSQL database.

    Returns:
        connection: A psycopg2 connection object.
    """
    try:
        connection = psycopg2.connect(
        database="postgres", 
        user="postgres",
        password="MurgZer0709*",
        host="localhost",
        port="5432"
        )
        return connection
    except Exception as e:
        # Print an error message if the connection fails
        print(f"Error connecting to the database: {e}")
        raise

# Save time for user by extracting key, structured EXIF metadata and insert in  database
# Function to insert EXIF metadata into database - ExifTool, Python (Piexif/PIL), or online viewers to find
        # orientation (1-8 rotation values) AND 
        # compass heading (decimal degrees)  - Key tags include: 
            # GPSImgDirection for bearing AND
            # GPSImgDirectionRef for True/Magnetic North
def insert_exif_metadata(media_id, exif_metadata):
    """
    Insert EXIF metadata into the pic_metadata_exif table.

    Args:
        media_id (str): The ID of the media file.
        exif_metadata (dict): A dictionary containing EXIF metadata.

    Returns:
        None
    """
    query = """
        INSERT INTO pic_metadata_exif (
            media_id, datetime_original, altitude, latitude, longitude, 
            compass_direction, orientation, JSON_metadata
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    connection = None  # Initialize connection to None
    try:
        connection = get_db_connection()  # Get a database connection
        cursor = connection.cursor()  # Create a cursor to execute the query

        # Execute the query with the provided EXIF metadata
            # compass heading (decimal degrees) 
            # orientation (1-8 rotation values)
        cursor.execute(
            query,
            (
                media_id,  # ID of the media file
                exif_metadata.get("DateTimeOriginal"),  # Original date and time of capture
                exif_metadata.get("Latitude"),  # Latitude from EXIF GPS data
                exif_metadata.get("Longitude"),  # Longitude from EXIF GPS data
                exif_metadata.get("GPSAltitude"),  # Altitude from EXIF GPS data
                exif_metadata.get("GPSImgDirection"),  # Compass heading (decimal degrees)
                exif_metadata.get("Orientation"),  # Camera rotation relative to ground (1-8 rotation values)
                Json(exif_metadata)  # Store the full metadata as JSON
            )
        )

        connection.commit()  # Commit the transaction
        cursor.close()  # Close the cursor
        connection.close()  # Close the database connection
        print("EXIF metadata inserted successfully.")

    except Exception as e:
        # Print an error message and roll back the transaction if an error occurs
        print(f"Error inserting EXIF metadata: {e}")
        if connection:
            connection.rollback()
        raise