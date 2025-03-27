"""
Service module for processing tumor predictions.

This module includes:
- Generating dummy tumor segmentation masks (simulating a UNet model).
- Storing predictions in the database.
"""

import os
from datetime import datetime
import numpy as np
from PIL import Image
from sqlalchemy.orm import Session

# Local Imports
from app.db.models.scan import Scan
from app.db.models.prediction import Prediction
from app.db.crud.crud_prediction import create_prediction
from app.schemas.prediction import PredictionCreate

# Directory for storing generated tumor masks
PREDICTION_DIR = "predictions/"
os.makedirs(PREDICTION_DIR, exist_ok=True)  # Ensure the directory exists


def generate_dummy_mask(image_path: str) -> str:
    """
    Simulates a UNet segmentation model by generating a random mask.

    Args:
        image_path (str): Path to the input MRI scan image.

    Returns:
        str: File path of the generated mask image.
    """
    # Convert MRI scan to grayscale
    img = Image.open(image_path).convert("L")

    # Generate a random mask
    mask_array = np.random.randint(0, 256, img.size, dtype=np.uint8)  # Random grayscale mask
    mask = Image.fromarray(mask_array.reshape(img.size[::-1]))  # Reshape to match original image

    # Save generated mask
    mask_filename = f"mask_{os.path.basename(image_path)}"
    mask_path = os.path.join(PREDICTION_DIR, mask_filename)
    mask.save(mask_path)

    return mask_path


def process_prediction(scan: Scan, db: Session) -> Prediction:
    """
    Runs the dummy tumor segmentation and stores the prediction in the database.

    Args:
        scan (Scan): The scan object for which prediction is being generated.
        db (Session): The active database session.

    Returns:
        Prediction: The created prediction entry in the database.
    """
    # Generate a fake tumor mask (simulating a segmentation model)
    result_path = generate_dummy_mask(scan.file_path)

    # Create a new prediction entry using PredictionCreate schema
    prediction_data = PredictionCreate(
        scan_id=scan.id,
        result_path=result_path,
        status="completed",
        created_at=datetime.utcnow()
    )

    # Save prediction to database
    prediction = create_prediction(db, prediction_data)

    return prediction
