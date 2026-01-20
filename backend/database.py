# database.py
# This file manages the database connection and queries.
# Use a library like SQLAlchemy or psycopg2 to interact with the SQL database.
# Example: Define functions to connect to the database and execute queries - Add a function to connect to the database and perform basic queries.
# Ensure secure handling of database credentials (e.g., use environment variables).

# Example SQLAlchemy setup:
# from sqlalchemy import create_engine
# DATABASE_URL = "sqlite:///example.db"
# engine = create_engine(DATABASE_URL)

# Function to connect to the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///example.db"  # Replace with your database URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
