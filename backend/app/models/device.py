from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    device_name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    power_rating = Column(Float, nullable=False)
    status = Column(Boolean, default=True)

    room = relationship("Room", back_populates="devices")
    energy_readings = relationship("EnergyReading", back_populates="device")
    anomalies = relationship("Anomaly", back_populates="device")



