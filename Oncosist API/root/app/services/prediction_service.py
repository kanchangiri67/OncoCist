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

import cv2
from app.ml_models.models_loader import get_unet_model, get_cnn_model, get_tumor_map
from app.ml_models.image_preprocessor import ImagePreprocessor

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
    Runs tumor segmentation and classification, saves the overlay image,
    and stores the prediction in the database.

    Args:
        scan (Scan): The MRI scan to process.
        db (Session): Active database session.

    Returns:
        Prediction: The stored prediction record.
    """
    # Run segmentation + classification
    overlay, tumor_type = analyze_mri(scan.file_path)

    # Save the overlay image
    overlay_filename = f"overlay_{os.path.basename(scan.file_path)}"
    result_path = os.path.join(PREDICTION_DIR, overlay_filename)

    # Ensure directory exists
    os.makedirs(os.path.dirname(result_path), exist_ok=True)

    # Convert overlay to image and save
    overlay_img = Image.fromarray(overlay.astype(np.uint8))
    overlay_img.save(result_path)

    # Create DB record
    prediction_data = PredictionCreate(
        scan_id=scan.id,
        tumor_type=tumor_type,
        result_path=result_path,
        status="completed",
        created_at=datetime.utcnow()
    )

    # Save to DB
    prediction = create_prediction(db, prediction_data)
    return prediction

def analyze_mri(image_path: str):
    image = cv2.imread(image_path)  # Load in color (default BGR)
    if image is None:
        raise ValueError("Could not load image from disk.")

    # Match Gradio behavior: Convert to grayscale explicitly
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Resize for both models
    resized = cv2.resize(image, (512, 512))
    normalized = ImagePreprocessor.normalize(resized)

    # Predict segmentation
    seg_input = normalized.reshape(1, 512, 512, 1)
    pred_mask = get_unet_model().predict(seg_input)[0]
    binary_mask = (pred_mask > 0.5).astype(np.uint8).squeeze()

    # Create overlay
    overlay = np.stack([normalized]*3, axis=-1)
    overlay[binary_mask == 1] = [255, 0, 0]  # Red

    # Predict tumor type
    class_input = normalized.reshape(1, 512, 512, 1)
    class_input = ImagePreprocessor.cnn_image_preprocessor(class_input)
    pred_class = np.argmax(get_cnn_model().predict(class_input), axis=1)[0]
    tumor_type = get_tumor_map()[pred_class]

    return overlay, tumor_type
