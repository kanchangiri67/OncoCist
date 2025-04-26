"""
MRI Scan History API.

This module provides:
- User-based scan history (recent and full).
- Patient-based scan history (recent and full).
- Deletion of scans (restricted to the uploading user).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

# Local Imports
from app.db.session import get_db
from app.db.models.scan import Scan
from app.db.models.patient import Patient
from app.db.models.user import User
from app.services.auth_service import get_current_user
from app.services.scan_service import format_scan_response

# Initialize router
router = APIRouter()

### USER-BASED SCAN HISTORY ###

@router.get("/user/recent", summary="Retrieve recent scans uploaded by the current user")
def get_recent_user_scans(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieves the 5 most recent scans uploaded by the authenticated user.
    """
    scans = (
        db.query(Scan)
        .options(joinedload(Scan.patient))
        .filter(Scan.user_id == current_user.id)
        .order_by(Scan.uploaded_at.desc())
        .limit(5)
        .all()
    )

    return {
        "user": {
            "user_id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        },
        "scans": format_scan_response(scans, include_patient=True, include_uploader=False)
    }


@router.get("/user/all", summary="Retrieve full scan history of the current user")
def get_all_user_scans(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieves the complete scan history uploaded by the authenticated user.
    """
    scans = (
        db.query(Scan)
        .options(joinedload(Scan.patient))
        .filter(Scan.user_id == current_user.id)
        .order_by(Scan.uploaded_at.desc())
        .all()
    )

    return {
        "user": {
            "user_id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        },
        "scans": format_scan_response(scans, include_patient=True, include_uploader=False)
    }


@router.get("/user/patients", summary="Retrieve all patients linked to the current user")
def get_patients_of_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieves all unique patients associated with the authenticated user's scans.
    """
    patient_ids = (
        db.query(Scan.patient_id)
        .filter(Scan.user_id == current_user.id)
        .distinct()
        .all()
    )
    patient_ids = [p[0] for p in patient_ids]
    patients = db.query(Patient).filter(Patient.id.in_(patient_ids)).all()

    patient_data = [
        {
            "patient_id": p.id,
            "patient_name": p.name,
            "patient_age": p.age,
            "patient_sex": p.sex
        }
        for p in patients
    ]

    return {
        "user": {
            "user_id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        },
        "patients": patient_data
    }


### PATIENT-BASED SCAN HISTORY ###

@router.get("/patient/{patient_id}/recent", summary="Retrieve recent scans of a patient")
def get_recent_patient_scans(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves the 5 most recent scans of a specific patient.
    """
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    scans = (
        db.query(Scan)
        .filter(Scan.patient_id == patient_id)
        .order_by(Scan.uploaded_at.desc())
        .limit(5)
        .all()
    )

    return {
        "patient": {
            "patient_id": patient.id,
            "patient_name": patient.name,
            "patient_age": patient.age,
            "patient_sex": patient.sex
        },
        "scans": format_scan_response(scans, include_patient=False, include_uploader=True)
    }


@router.get("/patient/{patient_id}/all", summary="Retrieve full scan history of a patient")
def get_all_patient_scans(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves the complete scan history of a specific patient.
    """
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    scans = (
        db.query(Scan)
        .filter(Scan.patient_id == patient_id)
        .order_by(Scan.uploaded_at.desc())
        .all()
    )

    return {
        "scans": format_scan_response(scans, include_patient=True, include_uploader=False)
    }


### DELETE SCAN (User Can Only Delete Their Own Scans) ###

@router.delete("/delete/{scan_id}", summary="Delete a scan (User-based permission)")
def delete_scan(scan_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Deletes an MRI scan uploaded by the authenticated user.
    """
    scan = db.query(Scan).filter(Scan.id == scan_id, Scan.user_id == current_user.id).first()

    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found or unauthorized to delete")

    db.delete(scan)
    db.commit()

    return {"message": "Scan deleted successfully"}
