"""
Service module for handling MRI scan uploads and formatting scan responses.

This module includes:
- File validation and storage for MRI scans.
- Database operations for storing scan details.
- Formatting scan data for API responses.
"""

import os
import shutil
from datetime import datetime, date
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

# Local Imports
from app.db.models.scan import Scan
from app.schemas.scan import ScanCreate

# Constants
UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "nii", "nii.gz"}


async def save_scan(file: UploadFile, patient, user_id: int, scan_date: date, db: Session) -> Scan:
    """
    Saves an MRI scan file to the filesystem and creates a database entry.

    Args:
        file (UploadFile): The uploaded MRI scan file.
        patient (Patient): The patient associated with the scan.
        user_id (int): The ID of the user uploading the scan.
        scan_date (date): The date of the scan.
        db (Session): Database session instance.

    Returns:
        Scan: The created scan entry in the database.
    """
    # Validate file extension
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file format.")

    # Define patient-specific upload directory
    patient_upload_dir = os.path.join(UPLOAD_DIR, f"patient_{patient.id}")
    os.makedirs(patient_upload_dir, exist_ok=True)  # Ensure directory exists

    # Define unique file storage path
    file_location = os.path.join(patient_upload_dir, f"{datetime.utcnow().timestamp()}_{file.filename}")

    # Save the file
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    # Create a new Scan entry linked to the patient
    scan_data = ScanCreate(
        patient_name=patient.name,
        age=patient.age,
        sex=patient.sex,
        scan_date=scan_date,
        file_path=file_location
    )
    new_scan = Scan(**scan_data.dict(), patient_id=patient.id, user_id=user_id)

    # Save to database
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)

    return new_scan


def format_scan_response(scans, include_patient: bool, include_uploader: bool = False) -> list:
    """
    Formats scan data for API responses.

    Args:
        scans (List[Scan]): List of scan objects from the database.
        include_patient (bool): Whether to include patient details in the response.
        include_uploader (bool, optional): Whether to include uploader details. Defaults to False.

    Returns:
        list: Formatted scan data for API responses.
    """
    formatted_scans = []
    for scan in scans:
        prediction = scan.prediction  # Fetch prediction details
        scan_data = {
            "scan_id": scan.id,
            "file_path": scan.file_path,
            "uploaded_at": scan.uploaded_at,
            "prediction_status": prediction.status if prediction else "pending",
            "prediction_result_path": prediction.result_path if prediction else None
        }

        if include_patient:
            scan_data["patient"] = {
                "patient_id": scan.patient.id,
                "patient_name": scan.patient.name,
                "patient_age": scan.patient.age,
                "patient_sex": scan.patient.sex
            }

        if include_uploader:
            scan_data["uploaded_by"] = {
                "user_id": scan.user.id,
                "username": scan.user.username,
                "email": scan.user.email
            }

        formatted_scans.append(scan_data)

    return formatted_scans
