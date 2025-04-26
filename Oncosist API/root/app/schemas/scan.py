"""
Scan Schema Definitions.

This module defines:
- Base schema for MRI scan details.
- Schema for creating a new scan.
- Schema for returning scan details.
"""

from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional


class ScanBase(BaseModel):
    """
    Base schema for MRI scans, used for inheritance.

    Attributes:
        patient_name (str): The full name of the patient.
        age (int): The age of the patient.
        sex (str): The gender of the patient (e.g., 'Male', 'Female', 'Other').
    """
    patient_name: str
    age: int
    sex: str


class ScanCreate(ScanBase):
    """
    Schema for creating a new scan entry.

    Attributes:
        file_path (str): The file path where the MRI scan is stored.
        scan_date (date): The date when the scan was taken.
        doctor_notes (Optional[str]): Notes entered by the doctor during scan upload.
    """
    file_path: str
    scan_date: date
    doctor_notes: Optional[str] = None  


class ScanResponse(ScanBase):
    """
    Schema for returning scan details.

    Attributes:
        id (int): Unique identifier for the scan.
        user_id (int): ID of the user (doctor) who uploaded the scan.
        scan_date (date): The date when the scan was taken.
        file_path (str): The location where the scan file is stored.
        uploaded_at (datetime): The timestamp when the scan was uploaded.
        doctor_notes (Optional[str]): Any notes from the doctor.
    """
    id: int
    user_id: int
    scan_date: date
    file_path: str
    uploaded_at: datetime
    doctor_notes: Optional[str] = None  

    model_config = ConfigDict(from_attributes=True)  
