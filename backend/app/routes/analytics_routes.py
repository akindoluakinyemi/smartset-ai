from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.database import SessionLocal
from backend.app.models.energy_reading import EnergyReading
from backend.app.schemas.analytics_schema import DeviceEnergySummary, TopDeviceConsumption
from backend.app.models.device import Device
from backend.app.models.household import Household
from backend.app.models.room import Room
from backend.app.models.device import Device
from backend.app.models.anomaly import Anomaly




router = APIRouter(prefix="/analytics", tags=["Analytics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/device/{device_id}/summary", response_model=DeviceEnergySummary)
def get_device_energy_summary(device_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            EnergyReading.device_id,
            func.sum(EnergyReading.power_consumption).label("total_consumption"),
            func.avg(EnergyReading.power_consumption).label("average_consumption"),
            func.max(EnergyReading.power_consumption).label("max_consumption"),
            func.min(EnergyReading.power_consumption).label("min_consumption"),
            func.count(EnergyReading.id).label("reading_count"),
        )
        .filter(EnergyReading.device_id == device_id)
        .group_by(EnergyReading.device_id)
        .first()
    )

    return result

@router.get("/top-devices", response_model=list[TopDeviceConsumption])
def get_top_energy_devices(db: Session = Depends(get_db)):
    results = (
        db.query(
            Device.id.label("device_id"),
            Device.device_name,
            Device.device_type,
            func.sum(EnergyReading.power_consumption).label("total_consumption"),
        )
        .join(EnergyReading, EnergyReading.device_id == Device.id)
        .group_by(Device.id, Device.device_name, Device.device_type)
        .order_by(func.sum(EnergyReading.power_consumption).desc())
        .limit(10)
        .all()
    )

    return results


@router.get("/peak-hours")
def get_peak_usage_hours(db: Session = Depends(get_db)):
    results = (
        db.query(
            func.extract("hour", EnergyReading.timestamp).label("hour"),
            func.sum(EnergyReading.power_consumption).label("total_consumption")
        )
        .group_by("hour")
        .order_by(func.sum(EnergyReading.power_consumption).desc())
        .all()
    )

    return [
        {
            "hour": int(row.hour),
            "total_consumption": float(row.total_consumption)
        }
        for row in results
    ]


@router.get("/most-anomalous-devices")
def get_most_anomalous_devices(db: Session = Depends(get_db)):
    results = (
        db.query(
            Device.device_name,
            Device.device_type,
            func.count(Anomaly.id).label("anomaly_count")
        )
        .join(Anomaly, Anomaly.device_id == Device.id)
        .group_by(Device.device_name, Device.device_type)
        .order_by(func.count(Anomaly.id).desc())
        .limit(10)
        .all()
    )

    return [
        {
            "device_name": row.device_name,
            "device_type": row.device_type,
            "anomaly_count": int(row.anomaly_count)
        }
        for row in results
    ]


@router.get("/top-households")
def get_top_households(db: Session = Depends(get_db)):
    results = (
        db.query(
            Household.household_name,
            Household.location,
            func.sum(EnergyReading.power_consumption).label("total_consumption")
        )
        .join(Room, Room.household_id == Household.id)
        .join(Device, Device.room_id == Room.id)
        .join(EnergyReading, EnergyReading.device_id == Device.id)
        .group_by(Household.household_name, Household.location)
        .order_by(func.sum(EnergyReading.power_consumption).desc())
        .all()
    )

    return [
        {
            "household_name": row.household_name,
            "location": row.location,
            "total_consumption": float(row.total_consumption)
        }
        for row in results
    ]
