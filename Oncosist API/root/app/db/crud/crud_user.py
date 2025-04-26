"""
CRUD operations for User management.

This module provides:
- Creating a new user with hashed passwords.
- Retrieving users by ID, email, or username.
- Filtering users by position with pagination.
"""

from sqlalchemy.orm import Session
from datetime import datetime
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def create_user(db: Session, user: UserCreate) -> User:
    """
    Creates a new user in the database.
    
    Args:
        db (Session): The database session.
        user (UserCreate): The user details from the request.

    Returns:
        User: The created user instance.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        position=user.position,
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Retrieves a user by their ID.
    
    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.

    Returns:
        User | None: The user instance if found, otherwise None.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Retrieves a user by their email.
    
    Args:
        db (Session): The database session.
        email (str): The email of the user.

    Returns:
        User | None: The user instance if found, otherwise None.
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Retrieves a user by their username.
    
    Args:
        db (Session): The database session.
        username (str): The username of the user.

    Returns:
        User | None: The user instance if found, otherwise None.
    """
    return db.query(User).filter(User.username == username).first()


def get_users_by_position(db: Session, position: str, limit: int = 10, skip: int = 0) -> list[User]:
    """
    Retrieves a list of users by their position (e.g., all doctors).
    
    Args:
        db (Session): The database session.
        position (str): The role of the users (e.g., "Doctor").
        limit (int, optional): Maximum number of users to retrieve. Defaults to 10.
        skip (int, optional): Number of records to skip (for pagination). Defaults to 0.

    Returns:
        list[User]: A list of user instances matching the position.
    """
    return db.query(User).filter(User.position == position).offset(skip).limit(limit).all()
