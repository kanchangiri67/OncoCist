"""
User Authentication API.

This module provides:
- User registration (sign-up).
- User login (returns access & refresh tokens).
- Token refresh for maintaining session persistence.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

# Local Imports
from app.db.session import get_db
from app.services.auth_service import register_user, login_user, refresh_access_token
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import TokenResponse

# Initialize router
router = APIRouter()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Register new user")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    API endpoint for user registration.

    This endpoint:
    - Creates a new user with a unique email and username.
    - Hashes the password before storing it.
    - Returns the created user details.

    Args:
        user_data (UserCreate): The user details from the request.
        db (Session): Database session dependency.

    Returns:
        UserResponse: The created user details.

    Raises:
        HTTPException: If the email is already registered.
    """
    new_user = register_user(db, user_data)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )
    return new_user


@router.post("/login", response_model=TokenResponse, summary="Authenticate user and return tokens")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    API endpoint for user login.

    This endpoint:
    - Authenticates a user using email and password.
    - Returns an access token and refresh token upon successful authentication.

    Args:
        form_data (OAuth2PasswordRequestForm): The login form containing email and password.
        db (Session): Database session dependency.

    Returns:
        TokenResponse: Contains access & refresh tokens.

    Raises:
        HTTPException: If authentication fails due to invalid credentials.
    """
    auth_result = login_user(db, form_data.username, form_data.password)
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    return auth_result


@router.post("/refresh", response_model=TokenResponse, summary="Refresh access token")
def refresh(token: str, db: Session = Depends(get_db)):
    """
    API endpoint for refreshing an expired access token.

    This endpoint:
    - Uses a valid refresh token to generate a new access token.
    - Ensures users remain logged in without requiring credentials again.

    Args:
        token (str): The refresh token provided by the client.
        db (Session): Database session dependency.

    Returns:
        TokenResponse: The new access token.

    Raises:
        HTTPException: If the refresh token is invalid or expired.
    """
    new_token = refresh_access_token(token)
    if not new_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    return new_token
