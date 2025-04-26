from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.scan import Scan
from app.db.models.patient import Patient
from app.db.models.user import User

router = APIRouter(prefix="/debug", tags=["Debug"])


@router.get("/scans")
def debug_all_scans(db: Session = Depends(get_db)):
    scans = db.query(Scan).all()
    results = []

    for scan in scans:
        patient = db.query(Patient).filter(Patient.id == scan.patient_id).first()
        user = db.query(User).filter(User.id == scan.user_id).first()

        results.append({
            "scan_id": scan.id,
            "file_path": scan.file_path,
            "uploaded_at": scan.uploaded_at,
            "user": user.username if user else "Unknown",
            "patient": {
                "id": patient.id,
                "name": patient.name,
                "age": patient.age,
                "sex": patient.sex
            } if patient else "Unknown"
        })

    return {"count": len(results), "scans": results}
