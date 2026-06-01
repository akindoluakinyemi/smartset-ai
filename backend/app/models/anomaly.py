from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.app.database import Base


class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    anomaly_score = Column(Float, nullable=False)
    anomaly_type = Column(String, nullable=False)
    detected_at = Column(DateTime, default=datetime.utcnow)

    device = relationship("Device", back_populates="anomalies")