from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal

from backend.app.models.household import Household
from backend.app.models.room import Room
from backend.app.models.device import Device
from backend.app.models.energy_reading import EnergyReading
from backend.app.models.anomaly import Anomaly

from backend.app.schemas.energy_reading_schema import (
    EnergyReadingResponse
)

router = APIRouter(
    prefix="/energy-readings",
    tags=["Energy Readings"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ----------------------------------------
# GET ALL ENERGY READINGS
# ----------------------------------------

@router.get(
    "/",
    response_model=list[EnergyReadingResponse]
)
def get_energy_readings(
    db: Session = Depends(get_db)
):

    return db.query(EnergyReading).all()


# ----------------------------------------
# GET ENERGY READINGS FOR ONE DEVICE
# ----------------------------------------

@router.get(
    "/device/{device_id}",
    response_model=list[EnergyReadingResponse]
)
def get_device_energy_readings(
    device_id: int,
    db: Session = Depends(get_db)
):

    return (
        db.query(EnergyReading)
        .filter(EnergyReading.device_id == device_id)
        .all()
    )


