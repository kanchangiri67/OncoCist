"""
Database session and engine configuration.

This module handles:
- Database connection setup.
- Creating a session factory.
- Ensuring tables are initialized.
- Providing a dependency function for database sessions.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException, status

# Local Imports
from app.core.config import settings
from app.db.base import Base  # Import all models to ensure table creation

# Configure database engine
if "sqlite" in settings.DATABASE_URL:
    engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(settings.DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Initializes the database by creating all tables if they do not exist.

    This function should be called at application startup.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Provides a database session dependency for FastAPI routes.

    Ensures proper session handling, including rollback on exceptions.

    Yields:
        Session: A database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
