"""
Token Schema Definitions.

This module defines:
- Schema for authentication token responses.
"""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """
    Schema for authentication token responses.

    Attributes:
        access_token (str): The JWT access token.
        refresh_token (str): The JWT refresh token.
        token_type (str): The token type (default: "bearer").
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
