"""
CRUD operations for MRI scan management.

This module provides:
- Creating a new MRI scan entry.
- Retrieving a scan by ID.
- Retrieving scans linked to a specific patient.
"""

from sqlalchemy.orm import Session
from app.db.models.scan import Scan
from app.schemas.scan import ScanCreate


def create_scan(db: Session, scan_data: ScanCreate) -> Scan:
    """
    Creates a new MRI scan entry in the database.

    Args:
        db (Session): The database session.
        scan_data (ScanCreate): The scan details.

    Returns:
        Scan: The created scan instance.
    """
    db_scan = Scan(**scan_data.dict())  # Convert Pydantic model to SQLAlchemy object
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan


def get_scan(db: Session, scan_id: int) -> Scan | None:
    """
    Retrieves a specific MRI scan by its ID.

    Args:
        db (Session): The database session.
        scan_id (int): The ID of the scan.

    Returns:
        Scan | None: The scan instance if found, otherwise None.
    """
    return db.query(Scan).filter(Scan.id == scan_id).first()


def get_scans_by_patient(db: Session, patient_id: int) -> list[Scan]:
    """
    Retrieves all MRI scans linked to a specific patient.

    Args:
        db (Session): The database session.
        patient_id (int): The ID of the patient.

    Returns:
        list[Scan]: A list of scans associated with the patient.
    """
    return db.query(Scan).filter(Scan.patient_id == patient_id).all()
