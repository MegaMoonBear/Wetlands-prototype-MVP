# config.py
# This file stores configuration settings for the backend.
# Tasks:
     # - Define database connection strings.
     # - Store constants for sandbox modules (e.g., API keys, file paths).
     # - Use environment variables for sensitive information.

# Example configuration:
# DATABASE_URL = "sqlite:///example.db"
# SECRET_KEY = "your-secret-key"

import os
from dotenv import load_dotenv
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///example.db")  # Default to SQLite if not set
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")  # Default secret key