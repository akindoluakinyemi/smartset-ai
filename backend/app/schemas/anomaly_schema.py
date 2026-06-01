from pydantic import BaseModel
from datetime import datetime


class AnomalyResponse(BaseModel):
    id: int
    device_id: int
    anomaly_score: float
    anomaly_type: str
    detected_at: datetime

    class Config:
        from_attributes = True