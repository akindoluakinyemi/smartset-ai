from pydantic import BaseModel


class DeviceResponse(BaseModel):
    id: int
    room_id: int
    device_name: str
    device_type: str
    power_rating: float
    status: bool

    class Config:
        from_attributes = True