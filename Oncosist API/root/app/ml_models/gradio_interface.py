# import gradio as gr
# import numpy as np
# import cv2
# from app.services.prediction_service import analyze_mri

import gradio as gr
import requests
import tempfile
from PIL import Image
from datetime import date

API_BASE = "http://127.0.0.1:8000"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrYW5jaGFuZ2lyaTY3QHlhaG9vLmNvbSIsImV4cCI6MTc0NTQ1NTI5OX0.rGNaFuru2f-58_Sl2DU2RaDO5f47EUfO09WiGa-gIrM" 

def analyze_via_api(image: Image.Image):
    # Step 1: Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        # Convert NumPy array to PIL image
        pil_image = Image.fromarray(image)
        pil_image.save(tmp.name)
        image_path = tmp.name

    # Step 2: Upload MRI scan
    upload_url = "http://127.0.0.1:8000/mri/upload"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    files = {"files": open(image_path, "rb")}

    params = {
        "patient_name": "Gradio User",
        "age": 30,
        "sex": "Male",
        "scan_date": str(date.today())
    }

    upload_res = requests.post(upload_url, headers=headers, files=files, params=params)

    print("UPLOAD RESPONSE:", upload_res.json())

    if upload_res.status_code != 200:
        return None, f"Upload failed: {upload_res.json()}"

    scan_id = upload_res.json()[0]["id"]

    # Step 3: Analyze MRI via backend
    analyze_url = f"{API_BASE}/predict/{scan_id}"
    analyze_res = requests.post(analyze_url, headers=headers)
    if analyze_res.status_code != 200:
        return None, f"Analysis failed: {analyze_res.json()}"

    result = analyze_res.json()
    overlay_img = Image.open(result["overlay_image_path"])
    tumor_type = result["tumor_type"]

    return overlay_img, tumor_type

# Gradio wrapper: input is a numpy image, output is overlay + label

def run_gradio_interface():
    interface = gr.Interface(
        fn=analyze_via_api,
        inputs=gr.Image(label="Upload Brain MRI", type="numpy"),
        outputs=[
            gr.Image(label="Tumor Mask Overlay", type="numpy"),
            gr.Label(label="Predicted Tumor Type")
        ],
        title="Brain Tumor Analysis",
        description="Upload a brain MRI to see the predicted tumor segmentation (U-Net) and classification (CNN)."
    )
    interface.launch(debug=True)

# Run the Gradio interface 
if __name__ == "__main__":
    run_gradio_interface()
