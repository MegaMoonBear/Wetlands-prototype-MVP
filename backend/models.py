# models.py
# This file defines the database models using raw SQL queries and psycopg2.
# Tasks:
# - Define database schema for storing AI responses and image metadata.
# - Provide functions to create tables and interact with the database.
# - Used by sandbox/database_saver.py to save data.

# Import psycopg2 for database interaction
import psycopg2  # psycopg2 is a library for interacting with PostgreSQL databases
from psycopg2 import sql  # sql module helps safely construct dynamic SQL queries
from dotenv import load_dotenv  # dotenv is used to load environment variables from a .env file
import os  # os provides functions to interact with the operating system, such as accessing environment variables

load_dotenv()  # Load environment variables from the .env file to make them accessible via os.getenv

# Database connection setup
# This function establishes a connection to the PostgreSQL database using credentials from environment variables.
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),  # Fetch the database name from the .env file
        user=os.getenv("DB_USER"),  # Fetch the database user from the .env file
        password=os.getenv("DB_PASSWORD"),  # Fetch the database password from the .env file
        host=os.getenv("DB_HOST", "localhost"),  # Default to localhost if DB_HOST is not set
        port=os.getenv("DB_PORT", "5432")  # Default to PostgreSQL's default port if DB_PORT is not set
    )

# Example function to create a table
def create_tables():
    connection = get_db_connection()  # Establish a database connection
    cursor = connection.cursor()  # Create a cursor to execute SQL commands
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,  # Auto-incrementing primary key
                email VARCHAR(255) UNIQUE NOT NULL  # Unique email field
            );

            CREATE TABLE IF NOT EXISTS images (
                id SERIAL PRIMARY KEY,  # Auto-incrementing primary key
                user_id INTEGER REFERENCES users(id),  # Foreign key to users table
                file_path VARCHAR(255) NOT NULL  # Path to the image file
            );
            """
        )
        connection.commit()  # Commit the transaction to save changes
    finally:
        cursor.close()  # Close the cursor to free resources
        connection.close()  # Close the connection to the database

# Example function to insert a user
# This function inserts a new user into the 'users' table and returns the generated user ID.
def insert_user(email):
    connection = get_db_connection()  # Establish a database connection
    cursor = connection.cursor()  # Create a cursor to execute SQL commands
    try:
        cursor.execute(
            "INSERT INTO users (email) VALUES (%s) RETURNING id;",  # Insert a new user and return the generated ID
            (email,)
        )
        result = cursor.fetchone()  # Fetch the result of the query
        if result is None:  # Ensure the query returned a result
            raise ValueError("No result returned from the database query.")
        user_id = result[0]  # Extract the user ID from the result
        connection.commit()  # Commit the transaction to save changes
        return user_id  # Return the generated user ID
    finally:
        cursor.close()  # Close the cursor to free resources
        connection.close()  # Close the connection to the database

# Example function to insert an image
# This function inserts a new image into the 'images' table and returns the generated image ID.
def insert_image(user_id, file_path):
    connection = get_db_connection()  # Establish a database connection
    cursor = connection.cursor()  # Create a cursor to execute SQL commands
    try:
        cursor.execute(
            "INSERT INTO images (user_id, file_path) VALUES (%s, %s) RETURNING id;",  # Insert a new image and return the generated ID
            (user_id, file_path)
        )
        result = cursor.fetchone()  # Fetch the result of the query
        if result is None:  # Ensure the query returned a result
            raise ValueError("No result returned from the database query.")
        image_id = result[0]  # Extract the image ID from the result
        connection.commit()  # Commit the transaction to save changes
        return image_id  # Return the generated image ID
    finally:
        cursor.close()  # Close the cursor to free resources
        connection.close()  # Close the connection to the database