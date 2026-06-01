from fastapi import FastAPI

from backend.app.routes.household_routes import router as household_router
from backend.app.routes.device_routes import router as device_router
from backend.app.routes.energy_routes import router as energy_router
from backend.app.routes.analytics_routes import router as analytics_router
from backend.app.routes.anomaly_routes import router as anomaly_router
from backend.app.routes.prediction_routes import router as prediction_router
from backend.app.routes.recommendation_routes import router as recommendation_router

app = FastAPI(
    title="SmartSet AI",
    description="AI-powered smart energy intelligence platform",
    version="0.1.0"
)


app.include_router(household_router)
app.include_router(device_router)
app.include_router(energy_router)
app.include_router(analytics_router)
app.include_router(anomaly_router)
app.include_router(prediction_router)
app.include_router(recommendation_router)

@app.get("/")
def root():
    return {"message": "SmartSet AI Backend Running"}