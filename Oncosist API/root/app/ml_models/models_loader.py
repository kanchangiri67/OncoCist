# app/ml_models/models_loader.py

import tensorflow as tf
from pathlib import Path
from app.ml_models.loss_functions import iou_metric, dice_loss, combined_loss

# Base directory of the model files
BASE_DIR = Path(__file__).resolve().parent

# Paths to model files
unet_path = BASE_DIR / "unet_model.keras"
cnn_path = BASE_DIR / "cnn_model.keras"

# Load U-Net model with custom objects
unet_model = tf.keras.models.load_model(
    unet_path,
    custom_objects={
        "iou_metric": iou_metric,
        "dice_loss": dice_loss,
        "combined_loss": combined_loss
    }
)

# Load CNN classification model
cnn_model = tf.keras.models.load_model(cnn_path)

# Tumor type map
tumor_map = {0: "Meningioma", 1: "Glioma", 2: "Pituitary Tumor"}

def get_unet_model():
    return unet_model

def get_cnn_model():
    return cnn_model

def get_tumor_map():
    return tumor_map
