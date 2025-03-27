"""
API Router Configuration.

This module:
- Registers all API endpoints.
- Organizes routes with prefixes and tags.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, upload, history, predict  

# Initialize the API router
router = APIRouter()

# Authentication (User sign-up and login)
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# MRI Upload (Scans create patients automatically)
router.include_router(upload.router, prefix="/mri", tags=["MRI Upload"])

# History & Deletion (User Services)
router.include_router(history.router, prefix="/history", tags=["History"])

# Tumor Prediction (Analyzed scans after U-Net process)
router.include_router(predict.router, prefix="/predict", tags=["Tumor Prediction"])
