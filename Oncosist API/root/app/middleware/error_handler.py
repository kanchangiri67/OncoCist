"""
Custom error handlers for FastAPI.

This module provides:
- Handling of HTTP exceptions (e.g., 404, 401).
- Handling of database errors (IntegrityError, SQLAlchemyError).
- Handling of unexpected internal errors.
"""

import logging
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Configure logging
logger = logging.getLogger(__name__)


def register_error_handlers(app: FastAPI):
    """
    Registers custom error handlers for different types of exceptions.

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        """
        Handles HTTP exceptions such as 404 Not Found, 401 Unauthorized.

        Args:
            request (Request): The incoming request object.
            exc (StarletteHTTPException): The HTTP exception.

        Returns:
            JSONResponse: A structured JSON error response.
        """
        logger.error(f"HTTP Error [{exc.status_code}]: {exc.detail} | Path: {request.url}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail, "status": exc.status_code}
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
        """
        Handles database integrity errors such as unique constraint violations.

        Args:
            request (Request): The incoming request object.
            exc (IntegrityError): The integrity error exception.

        Returns:
            JSONResponse: A structured JSON error response.
        """
        logger.error(f"Database Integrity Error: {exc.orig} | Path: {request.url}")
        return JSONResponse(
            status_code=400,
            content={"error": "Database integrity error", "detail": str(exc.orig)}
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        """
        Handles general SQLAlchemy database errors.

        Args:
            request (Request): The incoming request object.
            exc (SQLAlchemyError): The SQLAlchemy exception.

        Returns:
            JSONResponse: A structured JSON error response.
        """
        logger.error(f"Database Error: {str(exc)} | Path: {request.url}")
        return JSONResponse(
            status_code=500,
            content={"error": "Database error", "detail": str(exc)}
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Handles all unexpected errors.

        Args:
            request (Request): The incoming request object.
            exc (Exception): The generic exception.

        Returns:
            JSONResponse: A structured JSON error response.
        """
        logger.critical(f"Unexpected Error: {str(exc)} | Path: {request.url}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "detail": str(exc)}
        )
