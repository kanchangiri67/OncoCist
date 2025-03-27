"""
Tumor Prediction API.

This module handles:
- Running tumor segmentation on MRI scans.
- Returning stored predictions if available.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Local Imports
from app.db.session import get_db
from app.db.models.scan import Scan
from app.db.models.user import User
from app.schemas.prediction import PredictionResponse
from app.services.prediction_service import process_prediction
from app.db.crud.crud_prediction import get_prediction_by_scan
from app.services.auth_service import get_current_user

# Initialize router
router = APIRouter()


@router.post("/{scan_id}", response_model=PredictionResponse, summary="Predict tumor in MRI scan")
def predict_tumor(scan_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Triggers tumor segmentation for a given MRI scan.

    This endpoint:
    - Checks if the scan exists.
    - If a prediction already exists, returns it instead of re-processing.
    - If no prediction exists, runs segmentation and stores the result.

    Args:
        scan_id (int): The ID of the MRI scan.
        db (Session): Database session dependency.

    Returns:
        PredictionResponse: The prediction result.
    """
    # Check if scan exists
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    # Check if prediction already exists
    existing_prediction = get_prediction_by_scan(db, scan_id)
    if existing_prediction:
        return existing_prediction  # Return stored prediction instead of re-running

    # Run new prediction since it doesn't exist
    prediction = process_prediction(scan, db)
    return prediction
