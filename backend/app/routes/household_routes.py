from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import SessionLocal
from backend.app.models.household import Household
from backend.app.models.room import Room
from backend.app.models.device import Device
from backend.app.models.energy_reading import EnergyReading
from backend.app.models.anomaly import Anomaly
from backend.app.schemas.household_schema import HouseholdResponse


router = APIRouter(prefix="/households", tags=["Households"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[HouseholdResponse])
def get_households(db: Session = Depends(get_db)):
    households = db.query(Household).all()
    return households