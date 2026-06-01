import pandas as pd

from sklearn.ensemble import IsolationForest

from backend.app.database import SessionLocal

from backend.app.models.household import Household
from backend.app.models.room import Room
from backend.app.models.device import Device
from backend.app.models.energy_reading import EnergyReading
from backend.app.models.anomaly import Anomaly


def main():
    db = SessionLocal()

    try:
        db.query(Anomaly).delete()
        db.commit()

        readings = db.query(EnergyReading).all()

        data = []

        for reading in readings:
            data.append({
                "id": reading.id,
                "device_id": reading.device_id,
                "hour": reading.timestamp.hour,
                "power_consumption": reading.power_consumption,
                "voltage": reading.voltage,
                "current": reading.current,
            })

        df = pd.DataFrame(data)

        total_anomalies = 0

        for device_id, device_df in df.groupby("device_id"):
            if len(device_df) < 20:
                continue

            features = device_df[
                [
                    "hour",
                    "power_consumption",
                    "voltage",
                    "current",
                ]
            ]

            model = IsolationForest(
                contamination="auto",
                random_state=42,
            )

            model.fit(features)

            device_df = device_df.copy()
            device_df["anomaly_score"] = model.decision_function(features)

            score_mean = device_df["anomaly_score"].mean()
            score_std = device_df["anomaly_score"].std()

            threshold = score_mean - (2 * score_std)

            anomalies = device_df[
                device_df["anomaly_score"] < threshold
]

            for _, row in anomalies.iterrows():
                anomaly = Anomaly(
                    device_id=int(row["device_id"]),
                    anomaly_score=float(row["anomaly_score"]),
                    anomaly_type="Extreme Device Usage Pattern",
                )

                db.add(anomaly)

            total_anomalies += len(anomalies)

        db.commit()

        print(f"{total_anomalies} threshold-based anomalies detected.")

    except Exception as e:
        db.rollback()
        print(f"Error detecting anomalies: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    main()