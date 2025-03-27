"""
Database model for tumor detection predictions.

This module defines:
- Prediction metadata linked to MRI scans.
- Status tracking for model predictions.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Prediction(Base):
    """
    Represents tumor detection results linked to a specific MRI scan.

    Attributes:
        id (int): Unique identifier for the prediction.
        scan_id (int): ID of the related MRI scan.
        result_path (str): File path of the generated tumor mask.
        status (str): Prediction status ('pending', 'completed', 'failed').
        created_at (datetime): Timestamp of when the prediction was created.
    """
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False)  # Links prediction to a scan
    result_path = Column(String, nullable=False)  # Path to the generated tumor mask
    status = Column(String, default="pending")  # Possible values: 'pending', 'completed', 'failed'
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of prediction creation

    # Relationship to Scan model
    scan = relationship("Scan", back_populates="prediction")
