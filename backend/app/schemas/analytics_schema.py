from pydantic import BaseModel


class DeviceEnergySummary(BaseModel):
    device_id: int
    total_consumption: float
    average_consumption: float
    max_consumption: float
    min_consumption: float
    reading_count: int

class TopDeviceConsumption(BaseModel):
    device_id: int
    device_name: str
    device_type: str
    total_consumption: float