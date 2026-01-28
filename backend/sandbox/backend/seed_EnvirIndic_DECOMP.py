import os
import psycopg2
from datetime import datetime

# Database connection details
DATABASE_URL = "postgresql://postgres:MurgZer0709*@localhost:5432/postgres"

# Sample data
SECOND_IMAGE_NAME = "BirdsFromBelow.jpg"  # Replace with an actual image name from the images folder
SECOND_IMAGE_PATH = "backend/sandbox/images/" 
SAMPLE_TAGS = ["swamp", "bird", "flowing water", "muddy", "trees"] # Save for central Obs table
INDICATOR_UUID = "indicator-0000"
OBSERVATION_UUID = "observation-0000"
INDICATOR_TYPE = "plant" # Example types: plant, animal, water_flow
WATER_PICTURED = "Y" # boolean flag indicating water in image - more than kiddie pool
WATER_FLOWING = "Y" # boolean flag indicating flowing water (versus still)
WETLAND_CATEG = "freshwater" # Example types: freshwater, saltwater, brackish - restrict by location later
WETLAND_TYPE = "bog" # Example types: bog, marsh, swamp, fen - restrict by location later
RECOMMENDATION1 = "Plant"
RECOMMENDATION2 = "Animal"
RECOMMENDATION3 = "unknown species"
MEDIA_TYPE = "image" # ENUM: image, video, audio, text

# Updated second seed set - different pretend image
    # Why "second"? To simulate multiple entries in the database
    # Shouldn't 2nd set be records or rows in same table with  same attribute names?
SECOND_IMAGE_NAME = "AnimalWaterBranches.png"  
SECOND_IMAGE_PATH = "backend/sandbox/images/"  
SECOND_SAMPLE_TAGS = ["lake", "fish", "clear water", "rocks", "reeds"]
SECOND_INDICATOR_UUID = INDICATOR_UUID.replace("0000", "0001")
SECOND_OBSERVATION_UUID = OBSERVATION_UUID.replace("0000", "0001")
SECOND_INDICATOR_TYPE = INDICATOR_TYPE.replace("plant", "animal")
SECOND_WATER_PICTURED = "N"  # boolean flag indicating no water in image
SECOND_WATER_FLOWING = "N"  # boolean flag indicating no flowing water
SECOND_WETLAND_CATEG = WETLAND_CATEG.replace("freshwater", "unknown")
SECOND_WETLAND_TYPE = WETLAND_TYPE.replace("bog", "unknown")
SECOND_RECOMMENDATION1 = RECOMMENDATION1.replace("Plant", "Fish")
SECOND_RECOMMENDATION2 = RECOMMENDATION2.replace("Animal", "Insect")
SECOND_RECOMMENDATION3 = RECOMMENDATION3  # remains the same
SECOND_MEDIA_TYPE = MEDIA_TYPE  # ENUM: image, video, audio, text

def seed_database():
    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Iterate through images in the folder
        for image_name in os.listdir(IMAGES_FOLDER):
            image_path = os.path.join(IMAGES_FOLDER, image_name)
            if os.path.isfile(image_path):
                # Insert sample data into the database
                cursor.execute("""
                    INSERT INTO observations (submitted_at, user_id, media_type, storage_url, tags_user_device)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    datetime.now(),  # submitted_at
                    "test_user",  # user_id
                    MEDIA_TYPE,  # media_type
                    image_path,  # storage_url
                    SAMPLE_TAGS  # tags_user_device
                ))

        # Commit changes
        conn.commit()
        print("Database seeded successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

        # Example of how to use the second set in the database seeding
        if os.path.isfile(SECOND_IMAGE_PATH):
            cursor.execute("""
                INSERT INTO observations (submitted_at, user_id, media_type, storage_url, tags_user_device)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                datetime.now(),  # submitted_at
                "test_user_2",  # user_id
                SECOND_MEDIA_TYPE,  # media_type
                SECOND_IMAGE_PATH,  # storage_url
                SECOND_SAMPLE_TAGS  # tags_user_device
            ))

if __name__ == "__main__":
    seed_database()