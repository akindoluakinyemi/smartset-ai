from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.database import SessionLocal

from backend.app.models.household import Household
from backend.app.models.room import Room
from backend.app.models.device import Device
from backend.app.models.energy_reading import EnergyReading
from backend.app.models.anomaly import Anomaly


router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/device/{device_id}")
def get_device_recommendations(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()

    if device is None:
        raise HTTPException(
            status_code=404,
            detail=f"No device found with id {device_id}"
        )

    avg_power = (
        db.query(func.avg(EnergyReading.power_consumption))
        .filter(EnergyReading.device_id == device_id)
        .scalar()
    )

    anomaly_count = (
        db.query(func.count(Anomaly.id))
        .filter(Anomaly.device_id == device_id)
        .scalar()
    )

    avg_power = float(avg_power) if avg_power is not None else 0
    anomaly_count = int(anomaly_count) if anomaly_count is not None else 0

    recommendations = []

    if avg_power > device.power_rating * 0.8:
        recommendations.append(
            "This device has high average consumption. Consider reducing usage during peak hours."
        )

    if anomaly_count >= 50:
        recommendations.append(
            "This device has frequent anomalies. It may need inspection or usage review."
        )

    if device.device_type in ["Smart Heater", "Smart AC"]:
        recommendations.append(
            "Schedule this device during off-peak periods to reduce energy costs."
        )

    if not recommendations:
        recommendations.append(
            "This device appears to be operating within normal usage patterns."
        )

    return {
        "device_id": device_id,
        "device_name": device.device_name,
        "device_type": device.device_type,
        "average_power": round(avg_power, 2),
        "anomaly_count": anomaly_count,
        "recommendations": recommendations,
    }


