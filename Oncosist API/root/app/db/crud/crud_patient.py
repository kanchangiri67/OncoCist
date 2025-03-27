"""
CRUD operations for patient management.

This module provides:
- Creating a new patient record.
- Retrieving a patient by ID.
- Retrieving all patients from the database.
"""

from sqlalchemy.orm import Session
from app.db.models.patient import Patient
from app.schemas.patient import PatientCreate


def create_patient(db: Session, patient_data: PatientCreate) -> Patient:
    """
    Creates a new patient record in the database.

    Args:
        db (Session): The database session.
        patient_data (PatientCreate): The patient details.

    Returns:
        Patient: The created patient instance.
    """
    db_patient = Patient(**patient_data.dict())  # Convert Pydantic model to SQLAlchemy object
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_patient(db: Session, patient_id: int) -> Patient | None:
    """
    Retrieves a patient by their ID.

    Args:
        db (Session): The database session.
        patient_id (int): The ID of the patient.

    Returns:
        Patient | None: The patient instance if found, otherwise None.
    """
    return db.query(Patient).filter(Patient.id == patient_id).first()


def get_all_patients(db: Session) -> list[Patient]:
    """
    Retrieves all patients stored in the database.

    Args:
        db (Session): The database session.

    Returns:
        list[Patient]: A list of all patient records.
    """
    return db.query(Patient).all()
