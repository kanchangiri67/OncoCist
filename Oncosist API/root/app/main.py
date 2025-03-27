"""
Main entry point for the Oncosist API.

This module initializes:
- FastAPI application with middleware and error handling.
- Database setup.
- API route registration.
"""

from fastapi import FastAPI

# Local Imports
from app.api.v1.router import router
from app.db.session import init_db
from app.middleware.logging import CustomLoggingMiddleware
from app.middleware.error_handler import register_error_handlers

# Initialize FastAPI application
app = FastAPI(title="Oncosist API", version="1.0")


"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with a list of allowed domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
"""

@app.get("/", summary="API Root Endpoint")
async def root():
    """
    Root endpoint to verify if the API is running.

    Returns:
        dict: A simple message confirming API status.
    """
    return {"message": "Oncosist API is running! Visit /docs for Swagger UI."}


# Register error handlers
register_error_handlers(app)

# Add request/response logging middleware
app.add_middleware(CustomLoggingMiddleware)

# Ensure database tables are created
try:
    init_db()
except Exception as e:
    print(f" Database initialization failed: {str(e)}")


# Register API routes
app.include_router(router)
