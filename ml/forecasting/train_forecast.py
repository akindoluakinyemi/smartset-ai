import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

from backend.app.database import SessionLocal
from backend.app.models.household import Household
from backend.app.models.room import Room
from backend.app.models.device import Device
from backend.app.models.energy_reading import EnergyReading
from backend.app.models.anomaly import Anomaly


MODEL_PATH = "ml/saved_models/forecast_model.pkl"


def main():
    db = SessionLocal()

    try:
        readings = (
            db.query(EnergyReading, Device)
            .join(Device, EnergyReading.device_id == Device.id)
            .all()
        )

        data = []

        for reading, device in readings:
            data.append({
                "hour": reading.timestamp.hour,
                "day_of_week": reading.timestamp.weekday(),
                "device_type": device.device_type,
                "power_consumption": reading.power_consumption,
            })

        df = pd.DataFrame(data)

        X = df[["hour", "day_of_week", "device_type"]]
        y = df["power_consumption"]

        preprocessor = ColumnTransformer(
            transformers=[
                ("device_type_encoder", OneHotEncoder(handle_unknown="ignore"), ["device_type"])
            ],
            remainder="passthrough"
        )

        model = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
            ]
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        print(f"Mean Absolute Error: {mean_absolute_error(y_test, predictions):.2f} W")
        print(f"R² Score: {r2_score(y_test, predictions):.3f}")

        joblib.dump(model, MODEL_PATH)

        print(f"Model saved to: {MODEL_PATH}")

    finally:
        db.close()


if __name__ == "__main__":
    main()