"""
MRI Scan Upload API.

This module handles:
- Uploading MRI scans.
- Creating patient records if they do not exist.
- Associating scans with authenticated users.
"""

import os
from datetime import date
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

# Local Imports
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.patient import Patient
from app.schemas.scan import ScanResponse
from app.schemas.patient import PatientCreate
from app.services.auth_service import get_current_user
from app.db.crud.crud_patient import create_patient, get_patient
from app.services.scan_service import save_scan

# Initialize router
router = APIRouter()

# Define upload directory
UPLOAD_DIR = "uploads"
try:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
except OSError as e:
    raise HTTPException(status_code=500, detail=f"Failed to create upload directory: {str(e)}")


@router.post("/upload", response_model=List[ScanResponse], summary="Upload MRI scans")
async def upload_mri_scans(
    patient_name: str,
    age: int,
    sex: str,
    scan_date: date,
    files: List[UploadFile] = File(...),  # Accept multiple files
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # Requires authentication
):
    """
    Upload multiple MRI scan files and store metadata in the database.

    This endpoint:
    - Stores patient details in `patients` table if they don't exist.
    - Saves each scan inside `uploads/{patient_id}/` directory.
    - Links scans to the authenticated user.

    Args:
        patient_name (str): The patient's full name.
        age (int): The patient's age.
        sex (str): The patient's gender.
        scan_date (date): The date of the scan.
        files (List[UploadFile]): List of MRI scan files.
        db (Session): Database session dependency.
        current_user (User): Authenticated user.

    Returns:
        List[ScanResponse]: List of stored scan metadata.
    """

    # Retrieve user ID from authenticated user
    user_id = current_user.id

    # Check if patient exists, otherwise create a new patient entry
    patient = get_patient(db, patient_name)
    if not patient:
        patient_data = PatientCreate(name=patient_name, age=age, sex=sex)
        patient = create_patient(db=db, patient_data=patient_data)

    scan_responses = []
    
    for file in files:
        scan = await save_scan(file, patient, user_id, scan_date, db)
        scan_responses.append(scan)

    return scan_responses
