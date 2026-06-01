from pydantic import BaseModel
from datetime import datetime


class EnergyReadingResponse(BaseModel):
    id: int
    device_id: int
    timestamp: datetime
    power_consumption: float
    voltage: float
    current: float

    class Config:
        from_attributes = True