# File location: backend/models/database.py - Database connection configuration for Neon PostgreSQL
# This module provides connection pooling and helper functions for database operations.
# Updated for the Wetlands-prototype-MVP project.

import os
from dotenv import load_dotenv  # Loads environment variables from .env file
import asyncpg  # Async PostgreSQL driver for database operations
from typing import Optional

# Load environment variables from .env file
load_dotenv()  # Automatically finds and loads .env in the project directory

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")  # Retrieves DATABASE_URL from .env file

# Validate that DATABASE_URL exists
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables. Check your .env file.")


# ==================== Database Connection Pool ====================

# Global variable to store connection pool
db_pool: Optional[asyncpg.Pool] = None


async def get_database_pool() -> asyncpg.Pool:
    """
    Create and return a connection pool to the database.
    Connection pooling improves performance by reusing database connections.
    """
    global db_pool

    if db_pool is None:  # Only create pool if it doesn't exist
        db_pool = await asyncpg.create_pool(
            DATABASE_URL,  # Connection string from .env
            min_size=2,  # Minimum number of connections in pool
            max_size=10,  # Maximum number of connections in pool
            command_timeout=60  # Timeout for queries in seconds
        )
    return db_pool


async def close_database_pool():
    """
    Close the database connection pool.
    Call this when shutting down the application.
    """
    global db_pool

    if db_pool:
        await db_pool.close()  # Close all connections in pool
        db_pool = None


# ==================== Database Query Helper Functions ====================

async def execute_query(query: str, *args):
    """
    Execute a query that doesn't return results (INSERT, UPDATE, DELETE).

    Args:
        query: SQL query string
        *args: Query parameters (prevents SQL injection)

    Returns:
        Result of the query execution
    """
    pool = await get_database_pool()

    async with pool.acquire() as connection:  # Get connection from pool
        result = await connection.execute(query, *args)  # Execute query with parameters
        return result


async def fetch_one(query: str, *args):
    """
    Execute a query and return a single row.

    Args:
        query: SQL query string
        *args: Query parameters

    Returns:
        Single row as a Record object, or None if no results
    """
    pool = await get_database_pool()

    async with pool.acquire() as connection:
        row = await connection.fetchrow(query, *args)  # Fetch one row
        return dict(row) if row else None  # Convert to dict for easier use


async def fetch_all(query: str, *args):
    """
    Execute a query and return all rows.

    Args:
        query: SQL query string
        *args: Query parameters

    Returns:
        List of rows as dictionaries
    """
    pool = await get_database_pool()

    async with pool.acquire() as connection:
        rows = await connection.fetch(query, *args)  # Fetch all rows
        return [dict(row) for row in rows]  # Convert each row to dict


# ==================== Example Usage ====================
# Example 1: Insert data
# await execute_query("INSERT INTO submissions (user_ID, media_type) VALUES ($1, $2)", "user123", "image")

# Example 2: Fetch one record
# submission = await fetch_one("SELECT * FROM submissions WHERE id = $1", "some-uuid")

# Example 3: Fetch all records
# all_submissions = await fetch_all("SELECT * FROM submissions")
