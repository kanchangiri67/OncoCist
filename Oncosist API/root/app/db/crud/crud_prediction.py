"""
CRUD operations for managing tumor predictions.

This module provides:
- Creating a new tumor prediction entry.
- Retrieving a prediction linked to an MRI scan.
- Deleting a prediction entry.
"""

from sqlalchemy.orm import Session
from app.db.models.prediction import Prediction
from app.schemas.prediction import PredictionCreate


def create_prediction(db: Session, prediction_data: PredictionCreate) -> Prediction:
    """
    Creates a new tumor prediction entry in the database.

    Args:
        db (Session): The database session.
        prediction_data (PredictionCreate): The prediction details.

    Returns:
        Prediction: The created prediction instance.
    """
    db_prediction = Prediction(**prediction_data.dict())  # Convert Pydantic model to SQLAlchemy object
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction


def get_prediction_by_scan(db: Session, scan_id: int) -> Prediction | None:
    """
    Retrieves the tumor prediction associated with a specific MRI scan.

    Args:
        db (Session): The database session.
        scan_id (int): The ID of the MRI scan.

    Returns:
        Prediction | None: The prediction instance if found, otherwise None.
    """
    return db.query(Prediction).filter(Prediction.scan_id == scan_id).first()


def delete_prediction(db: Session, scan_id: int) -> dict:
    """
    Deletes a prediction linked to a specific MRI scan.

    Args:
        db (Session): The database session.
        scan_id (int): The ID of the MRI scan.

    Returns:
        dict: A message indicating whether the deletion was successful.
    """
    prediction = get_prediction_by_scan(db, scan_id)
    if prediction:
        db.delete(prediction)
        db.commit()
        return {"message": "Prediction deleted successfully"}
    return {"message": "Prediction not found"}
