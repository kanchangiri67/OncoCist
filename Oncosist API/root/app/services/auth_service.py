"""
Authentication service module.

This module includes:
- User registration with unique email validation.
- User authentication and password verification.
- JWT-based login with access and refresh token generation.
- Access token refresh handling.
- Retrieving the current user from the JWT token.
"""

from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Local imports
from app.db.crud.crud_user import get_user_by_email, create_user
from app.core.security import (
    verify_password, get_password_hash, 
    create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
)
from app.schemas.user import UserCreate, UserResponse
from app.db.session import get_db
from app.db.models.user import User

# Token expiration settings
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

def register_user(db: Session, user_data: UserCreate) -> UserResponse:
    """
    Registers a new user (doctor) and ensures uniqueness of email and username.

    Args:
        db (Session): The database session.
        user_data (UserCreate): The user data from the request.

    Returns:
        UserResponse: The newly created user data.
    
    Raises:
        HTTPException: If the email or username is already taken.
    """
    # Check if email is already registered
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )

    # Check if username is already taken
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken"
        )

    # Create the user
    new_user = create_user(db, user_data)
    return UserResponse.model_validate(new_user)


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """
    Authenticates a user by verifying email and password.

    Args:
        db (Session): The database session.
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        User | None: The authenticated user object if valid, otherwise None.
    """
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None  # Invalid credentials
    return user


def login_user(db: Session, email: str, password: str) -> dict | None:
    """
    Handles user login and token generation.

    Args:
        db (Session): The database session.
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        dict | None: Dictionary containing access & refresh tokens if authentication is successful.
    """
    user = authenticate_user(db, email, password)
    if not user:
        return None  # Authentication failed

    # Generate tokens with expiration times
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": user.email}, expires_delta=refresh_token_expires)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }


def refresh_access_token(refresh_token: str) -> dict | None:
    """
    Generates a new access token using a valid refresh token.

    Args:
        refresh_token (str): The refresh token.

    Returns:
        dict | None: Dictionary containing the new access token.
    """
    payload = decode_refresh_token(refresh_token)
    if not payload:
        return None  # Invalid refresh token

    email = payload.get("sub")
    if not email:
        return None  # Malformed token

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(data={"sub": email}, expires_delta=access_token_expires)

    return {"access_token": new_access_token, "token_type": "bearer"}


# OAuth2 Password Bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Extracts the user from the JWT access token and verifies existence.

    Args:
        token (str): The JWT access token.
        db (Session): The database session.

    Returns:
        User: The authenticated user.

    Raises:
        HTTPException: If the credentials are invalid or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception

    email: str = payload.get("sub")
    if not email:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
