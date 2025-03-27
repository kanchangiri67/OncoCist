"""
Base model for SQLAlchemy ORM.

This module defines:
- A common base class for all database models.
- Automatic model recognition by SQLAlchemy.
"""

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Base class for all database models."""
    pass

# Import all models to ensure SQLAlchemy recognizes them
from app.db.models.user import User
from app.db.models.scan import Scan
from app.db.models.patient import Patient
from app.db.models.prediction import Prediction
