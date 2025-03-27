"""
Security module for handling authentication, password hashing, and JWT token generation.

This module includes:
- Password hashing and verification using bcrypt.
- JWT access and refresh token creation and decoding.
- Environment variable loading for security keys.
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

# Local imports
from app.db.models.user import User
from app.db.session import get_db

# Load environment variables from .env file
load_dotenv()

# Retrieve secret keys from environment
SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")

# Ensure that secret keys are available
if not SECRET_KEY or not REFRESH_SECRET_KEY:
    raise ValueError("ERROR: SECRET_KEY and REFRESH_SECRET_KEY must be set in .env!")

# JWT Configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Access token expires in 1 hour
REFRESH_TOKEN_EXPIRE_DAYS = 7  # Refresh token expires in 7 days

# Password hashing setup using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Hashes a password using bcrypt.
    
    Args:
        password (str): The plaintext password.
    
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that a given plain text password matches a stored hashed password.
    
    Args:
        plain_password (str): The plaintext password.
        hashed_password (str): The hashed password stored in the database.
    
    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Generates a JWT access token.
    
    Args:
        data (dict): The data to be encoded in the token.
        expires_delta (timedelta, optional): The duration until the token expires.
    
    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Generates a JWT refresh token.
    
    Args:
        data (dict): The data to be encoded in the refresh token.
        expires_delta (timedelta, optional): The duration until the token expires.
    
    Returns:
        str: The encoded JWT refresh token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    """
    Decodes and verifies a JWT access token.
    
    Args:
        token (str): The encoded JWT access token.
    
    Returns:
        dict | None: Decoded token data if valid, otherwise None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def decode_refresh_token(token: str):
    """
    Decodes and verifies a JWT refresh token.
    
    Args:
        token (str): The encoded JWT refresh token.
    
    Returns:
        dict | None: Decoded token data if valid, otherwise None.
    """
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
