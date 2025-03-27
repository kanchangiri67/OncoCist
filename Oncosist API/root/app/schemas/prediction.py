"""
Prediction Schema Definitions.

This module defines:
- Base schema for tumor predictions.
- Schema for creating a new prediction.
- Schema for returning prediction details.
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PredictionBase(BaseModel):
    """
    Base schema for tumor predictions.

    Attributes:
        scan_id (int): The ID of the related MRI scan.
        result_path (str): File path where the prediction result is stored.
        status (str): The status of the prediction ('pending', 'completed', 'failed').
    """
    scan_id: int
    result_path: str
    status: str  # 'pending', 'completed', 'failed'


class PredictionCreate(PredictionBase):
    """
    Schema for creating a new prediction.
    Inherits all fields from PredictionBase.
    """
    pass


class PredictionResponse(PredictionBase):
    """
    Schema for returning prediction details.

    Attributes:
        id (int): Unique identifier for the prediction.
        created_at (datetime): Timestamp when the prediction was created.
    """
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  # Enables ORM serialization
