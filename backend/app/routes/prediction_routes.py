import joblib
import pandas as pd

from fastapi import APIRouter

from backend.app.schemas.prediction_schema import (
    ForecastRequest,
    ForecastResponse,
)


MODEL_PATH = "ml/saved_models/forecast_model.pkl"

router = APIRouter(prefix="/predict", tags=["Predictions"])

model = joblib.load(MODEL_PATH)


@router.post("/forecast", response_model=ForecastResponse)
def forecast_power(request: ForecastRequest):
    input_data = pd.DataFrame([{
        "hour": request.hour,
        "day_of_week": int(request.day_of_week),
        "device_type": request.device_type.value,
    }])

    prediction = model.predict(input_data)[0]

    return ForecastResponse(
        hour=request.hour,
        day_of_week=int(request.day_of_week),
        device_type=request.device_type.value,
        predicted_power_consumption=round(float(prediction), 2),
    )