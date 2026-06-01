from enum import Enum
from pydantic import BaseModel, Field


class DayOfWeek(int, Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6


class DeviceType(str, Enum):
    smart_ac = "Smart AC"
    smart_tv = "Smart TV"
    smart_light = "Smart Light"
    smart_fridge = "Smart Fridge"
    smart_heater = "Smart Heater"


class ForecastRequest(BaseModel):
    hour: int = Field(..., ge=0, le=23)
    day_of_week: DayOfWeek
    device_type: DeviceType


class ForecastResponse(BaseModel):
    hour: int
    day_of_week: int
    device_type: str
    predicted_power_consumption: float