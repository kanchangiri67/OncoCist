"""
Patient Schema Definitions.

This module defines:
- Base schema for patient details.
- Schema for creating a new patient.
- Schema for returning patient details with scan history.
"""

from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class PatientBase(BaseModel):
    """
    Base schema for the Patient model.

    Attributes:
        name (str): Full name of the patient.
        age (int): Age of the patient.
        sex (str): Gender of the patient ('Male', 'Female', 'Other').
    """
    name: str
    age: int
    sex: str  # 'Male', 'Female', 'Other'


class PatientCreate(PatientBase):
    """
    Schema for creating a new patient.
    Inherits all fields from PatientBase.
    """
    pass


class PatientResponse(PatientBase):
    """
    Schema for returning patient details.

    Attributes:
        id (int): Unique identifier for the patient.
        scans (Optional[List[int]]): List of scan IDs associated with the patient.
    """
    id: int
    scans: Optional[List[int]]  # List of scan IDs linked to this patient

    model_config = ConfigDict(from_attributes=True)  # Enables ORM serialization
