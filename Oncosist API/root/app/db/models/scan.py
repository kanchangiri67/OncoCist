"""
Database model for MRI scans.

This module defines:
- Scan metadata including patient details, uploader, and file storage.
- Relationships to users, patients, and predictions.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
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
    """
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Links scan to uploader
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)  # Links scan to patient
    patient_name = Column(String, nullable=True)  # Optional field for patient's name
    age = Column(Integer, nullable=False)  # Patient's age
    sex = Column(String, nullable=False)  # Gender of the patient
    scan_date = Column(DateTime, nullable=False)  # Date when scan was taken
    uploaded_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of scan upload
    file_path = Column(String, nullable=False)  # File storage location

    # Relationships
    user = relationship("User", back_populates="scans")  # Links to User model
    patient = relationship("Patient", back_populates="scans")  # Links to Patient model
    prediction = relationship("Prediction", back_populates="scan", uselist=False, cascade="all, delete-orphan")  # Links to Prediction model
