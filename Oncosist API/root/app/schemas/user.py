"""
User Schema Definitions.

This module defines:
- Base user schema for inheritance.
- Schema for user creation (signup).
- Schema for user response (excluding password).
"""

from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    """
    Base schema for User, used for inheritance.

    Attributes:
        username (str): The unique username of the user.
        email (EmailStr): The user's email (validated).
        full_name (str): The full name of the user.
        position (str): The role or position of the user.
    """
    username: str
    email: EmailStr
    full_name: str
    position: str


class UserCreate(UserBase):
    """
    Schema for creating a new user (signup request).

    Attributes:
        password (str): The user's password (hashed before storage).
    """
    password: str


class UserResponse(UserBase):
    """
    Schema for returning user details (excluding password).

    Attributes:
        id (int): Unique identifier for the user.
        created_at (datetime): Timestamp when the user was created.
    """
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  # Allows ORM conversion for response models
