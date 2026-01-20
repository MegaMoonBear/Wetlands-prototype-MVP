# database.py
# This file manages the database connection and queries using psycopg2.
# Example: Define functions to connect to the database and execute queries.
# Ensure secure handling of database credentials (e.g., use environment variables).

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

# Example function to execute a query
def execute_query(query, params=None):
    connection = get_db_connection()  # Establish a database connection
    cursor = connection.cursor()  # Create a cursor to execute SQL commands
    try:
        cursor.execute(query, params)  # Execute the provided SQL query with parameters
        connection.commit()  # Commit the transaction to save changes
    finally:
        cursor.close()  # Close the cursor to free resources
        connection.close()  # Close the connection to the database

# Example function to fetch data
def fetch_data(query, params=None):
    connection = get_db_connection()  # Establish a database connection
    cursor = connection.cursor()  # Create a cursor to execute SQL commands
    try:
        cursor.execute(query, params)  # Execute the provided SQL query with parameters
        results = cursor.fetchall()  # Fetch all rows from the query result
        return results
    finally:
        cursor.close()  # Close the cursor to free resources
        connection.close()  # Close the connection to the database
