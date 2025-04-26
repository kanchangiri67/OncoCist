# migrate_doctor_notes.py

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from sqlalchemy import text
from app.db.session import SessionLocal

def add_doctor_notes_column():
    db = SessionLocal()
    try:
        print("Running ALTER TABLE...")
        db.execute(text("ALTER TABLE scans ADD COLUMN doctor_notes TEXT"))
        db.commit()
        print("Doctor_notes column added successfully.")
    except Exception as e:
        print("Migration failed:", e)
    finally:
        db.close()

if __name__ == "__main__":
    add_doctor_notes_column()
