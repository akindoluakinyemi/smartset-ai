from pydantic import BaseModel
from datetime import datetime


class HouseholdResponse(BaseModel):
    id: int
    household_name: str
    location: str | None
    created_at: datetime

    class Config:
        from_attributes = True