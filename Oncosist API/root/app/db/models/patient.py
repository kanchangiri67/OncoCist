"""
Database model for storing patient details.

This module defines:
- Patient demographics.
- Relationships between patients and their MRI scans.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Patient(Base):
    """
    Represents a patient in the system.

    Attributes:
        id (int): Unique identifier for the patient.
        name (str): Full name of the patient.
        age (int): Age of the patient.
        sex (str): Gender of the patient ('Male', 'Female', 'Other').
    """
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Unique patient ID
    name = Column(String, nullable=False)  # Patient's full name
    age = Column(Integer, nullable=False)  # Patient's age
    sex = Column(String, nullable=False)  # Patient's gender

    # Relationship to the Scan model (one-to-many)
    scans = relationship("Scan", back_populates="patient", cascade="all, delete-orphan")
