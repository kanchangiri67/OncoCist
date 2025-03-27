"""
Database model for users (doctors).

This module defines:
- User authentication details.
- Relationships between users and their uploaded scans.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    """
    Represents a user (doctor) in the system.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Unique username for login.
        email (str): Unique email address.
        hashed_password (str): Securely stored hashed password.
        full_name (str): Full name of the user.
        position (str): User's role (default: "Doctor").
        created_at (datetime): Timestamp of account creation.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)  # Unique username for login
    email = Column(String, unique=True, index=True, nullable=False)  # Unique email for authentication
    hashed_password = Column(String, nullable=False)  # Securely hashed password
    full_name = Column(String, nullable=False)  # User's full name
    position = Column(String, nullable=False, default="Doctor")  # User role in the system
    created_at = Column(DateTime, default=datetime.utcnow)  # Account creation timestamp

    # Relationship to scans
    scans = relationship("Scan", back_populates="user", cascade="all, delete-orphan")
