"""
MRI Scan Upload API.

This module handles:
- Uploading MRI scans.
- Creating patient records if they do not exist.
- Associating scans with authenticated users.
"""

import os
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
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
    patient_name: str = Form(...),
    age: int = Form(...),
    sex: str = Form(...),
    scan_date: date = Form(...),
    doctor_notes: Optional[str] = Form(None),  # ✅ Added doctor notes as form input
    files: List[UploadFile] = File(...),  # Accept multiple files
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload multiple MRI scan files and store metadata in the database.

    This endpoint:
    - Stores patient details in `patients` table if they don't exist.
    - Saves each scan inside `uploads/{patient_id}/` directory.
    - Links scans to the authenticated user.
    - Stores doctor notes if provided.

    Returns:
        List[ScanResponse]: List of stored scan metadata.
    """

    user_id = current_user.id

    patient = get_patient(db, patient_name)
    if not patient:
        patient_data = PatientCreate(name=patient_name, age=age, sex=sex)
        patient = create_patient(db=db, patient_data=patient_data)

    scan_responses = []

    for file in files:
        scan = await save_scan(file, patient, user_id, scan_date, db, doctor_notes=doctor_notes)
        scan_responses.append(scan)

    return scan_responses
