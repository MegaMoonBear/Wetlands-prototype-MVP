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
            dbname="your_database_name",  # Replace with your database name
            user="your_username",  # Replace with your database username
            password="your_password",  # Replace with your database password
            host="localhost",  # Replace with your database host
            port="5432"  # Replace with your database port
        )
        return connection
    except Exception as e:
        # Print an error message if the connection fails
        print(f"Error connecting to the database: {e}")
        raise

# Function to insert EXIF metadata into the database
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
            media_id, camera_make, camera_model, datetime_original, altitude,
            orientation, exposure_time, f_number, iso, focal_length, flash, additional_metadata
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    try:
        connection = get_db_connection()  # Get a database connection
        cursor = connection.cursor()  # Create a cursor to execute the query

        # Execute the query with the provided EXIF metadata
        cursor.execute(
            query,
            (
                media_id,  # ID of the media file
                exif_metadata.get("Make"),  # Camera manufacturer
                exif_metadata.get("Model"),  # Camera model
                exif_metadata.get("DateTimeOriginal"),  # Original date and time of capture
                exif_metadata.get("GPSAltitude"),  # Altitude from EXIF GPS data
                exif_metadata.get("Orientation"),  # Orientation of the image
                exif_metadata.get("ExposureTime"),  # Exposure time (e.g., "1/200")
                exif_metadata.get("FNumber"),  # Aperture value (e.g., "f/2.8")
                exif_metadata.get("ISOSpeedRatings"),  # ISO speed
                exif_metadata.get("FocalLength"),  # Focal length (e.g., "50mm")
                exif_metadata.get("Flash"),  # Flash information (e.g., "Fired")
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