"""
Database model for MRI scans.

This module defines:
- Scan metadata including patient details, uploader, and file storage.
- Relationships to users, patients, and predictions.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base


class Scan(Base):
    """
    Represents an MRI scan record in the database.

    Attributes:
        id (int): Unique identifier for the scan.
        user_id (int): ID of the user (doctor) who uploaded the scan.
        patient_id (int): ID of the associated patient.
        patient_name (str): Name of the patient (optional).
        age (int): Age of the patient.
        sex (str): Gender of the patient ('Male', 'Female', 'Other').
        scan_date (datetime): The date when the scan was taken.
        uploaded_at (datetime): Timestamp when the scan was uploaded.
        file_path (str): The location where the scan file is stored.
        doctor_notes (str): Optional notes added by the doctor.
    """
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    patient_name = Column(String, nullable=True)
    age = Column(Integer, nullable=False)
    sex = Column(String, nullable=False)
    scan_date = Column(DateTime, nullable=False)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    file_path = Column(String, nullable=False)
    doctor_notes = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="scans")
    patient = relationship("Patient", back_populates="scans")
    prediction = relationship("Prediction", back_populates="scan", uselist=False, cascade="all, delete-orphan")
