# models.py
# This file defines the database models using raw SQL queries and psycopg2.
# Example: Create functions to interact with the database tables directly.
# Ensure functions are consistent with the database schema.

# Import psycopg2 for database interaction
import psycopg2  # psycopg2 is a library for interacting with PostgreSQL databases
from psycopg2 import sql  # sql module helps safely construct dynamic SQL queries

# Database connection setup
# Replace with your actual database credentials
def get_db_connection():
    return psycopg2.connect(
        dbname="your_database_name",  # Name of the PostgreSQL database
        user="your_username",  # Username for database authentication
        password="your_password",  # Password for database authentication
        host="localhost",  # Host where the database server is running
        port="5432"  # Default port for PostgreSQL
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
def insert_user(email):
    connection = get_db_connection()  # Establish a database connection
    cursor = connection.cursor()  # Create a cursor to execute SQL commands
    try:
        cursor.execute(
            "INSERT INTO users (email) VALUES (%s) RETURNING id;",  # Insert a new user
            (email,)
        )
        user_id = cursor.fetchone()[0]  # Fetch the generated user ID
        connection.commit()  # Commit the transaction to save changes
        return user_id
    finally:
        cursor.close()  # Close the cursor to free resources
        connection.close()  # Close the connection to the database

# Example function to insert an image
def insert_image(user_id, file_path):
    connection = get_db_connection()  # Establish a database connection
    cursor = connection.cursor()  # Create a cursor to execute SQL commands
    try:
        cursor.execute(
            "INSERT INTO images (user_id, file_path) VALUES (%s, %s) RETURNING id;",  # Insert a new image
            (user_id, file_path)
        )
        image_id = cursor.fetchone()[0]  # Fetch the generated image ID
        connection.commit()  # Commit the transaction to save changes
        return image_id
    finally:
        cursor.close()  # Close the cursor to free resources
        connection.close()  # Close the connection to the database