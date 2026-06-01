from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal

from backend.app.models.household import Household
from backend.app.models.room import Room
from backend.app.models.device import Device
from backend.app.models.energy_reading import EnergyReading
from backend.app.models.anomaly import Anomaly

from backend.app.schemas.anomaly_schema import AnomalyResponse


router = APIRouter(prefix="/anomalies", tags=["Anomalies"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[AnomalyResponse])
def get_anomalies(db: Session = Depends(get_db)):
    return db.query(Anomaly).all()


@router.get("/device/{device_id}", response_model=list[AnomalyResponse])
def get_device_anomalies(device_id: int, db: Session = Depends(get_db)):
    return db.query(Anomaly).filter(Anomaly.device_id == device_id).all()