""" 
Main entry point for the Oncosist API.

This module initializes:
- FastAPI application with middleware and error handling.
- Database setup.
- API route registration.
- Static file serving for prediction overlays.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Local Imports
from app.api.v1.router import router
from app.db.session import init_db
from app.middleware.logging import CustomLoggingMiddleware
from app.middleware.error_handler import register_error_handlers
from app.routers import debug_scans  

# Initialize FastAPI application
app = FastAPI(title="Oncosist API", version="1.0")

# Allow static image previews (e.g., overlay images)
PREDICTION_DIR = "predictions"
os.makedirs(PREDICTION_DIR, exist_ok=True)
app.mount("/predictions", StaticFiles(directory=PREDICTION_DIR), name="predictions")

# Optional: if scans are stored in uploads/
UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

# Allow frontend access via CORS (adjust domains as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint for basic API health check
@app.get("/", summary="API Root Endpoint")
async def root():
    return {"message": "Oncosist API is running! Visit /docs for Swagger UI."}

# Register global error handlers
register_error_handlers(app)

# Add custom request/response logging middleware
app.add_middleware(CustomLoggingMiddleware)

# Initialize DB tables on first launch
try:
    init_db()
except Exception as e:
    print(f"Database initialization failed: {str(e)}")

# Register all versioned API routes
app.include_router(router)

# Register debug router
app.include_router(debug_scans.router)
