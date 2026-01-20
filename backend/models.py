# models.py
# This file defines the database models if using an ORM like SQLAlchemy.
# Example: Create classes that map to database tables and define relationships.
# Use SQLAlchemy's Base class to define models.
# Ensure models are consistent with the database schema.

# Example SQLAlchemy model:
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String
# Base = declarative_base()
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)

# What to Include in models.py:
# Table Definitions:
# Define classes for each table.
# Specify attributes (columns) with their data types and constraints.
# Schema Information:
# Use SQLAlchemy's Base class to define the schema.
# Include relationships if needed.

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    # name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_path = Column(String, nullable=False)