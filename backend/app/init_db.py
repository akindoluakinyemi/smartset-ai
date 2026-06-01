from backend.app.database import Base, engine

from backend.app.models.household import Household
from backend.app.models.room import Room
from backend.app.models.device import Device
from backend.app.models.energy_reading import EnergyReading
from backend.app.models.anomaly import Anomaly


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables checked/created successfully.")


if __name__ == "__main__":
    init_db()
