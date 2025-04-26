# app/api/v1/endpoints/predict.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Local Imports
from app.db.session import get_db
from app.db.models.scan import Scan
from app.db.models.user import User
from app.db.crud.crud_prediction import get_prediction_by_scan
from app.services.prediction_service import process_prediction
from app.services.auth_service import get_current_user

router = APIRouter()


@router.post("/{scan_id}", summary="Predict tumor in MRI scan")
def predict_tumor(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Triggers tumor segmentation and classification for a given MRI scan.

    This endpoint:
    - Checks if the scan exists
    - Returns cached prediction if already available
    - Otherwise runs the ML models and stores the result
    """
    # Check if scan exists
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    # Return cached prediction if available
    prediction = get_prediction_by_scan(db, scan_id)
    if prediction:
        return {
            "tumor_type": prediction.tumor_type,
            "overlay_image_path": prediction.result_path
        }

    # Otherwise run ML model
    prediction = process_prediction(scan, db)

    return {
        "tumor_type": prediction.tumor_type,
        "overlay_image_path": prediction.result_path
    }
