from sklearn.ensemble import IsolationForest
import pandas as pd
import joblib
from config import ANOMALY_MODEL_PATH

FEATURES = ["cpu_percent", "ram_percent", "disk_percent"]

def train_model(csv_path="storage/metrics.csv"):
    df = pd.read_csv(csv_path)
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(df[FEATURES])
    joblib.dump(model, ANOMALY_MODEL_PATH)
    return model

def detect_anomaly(model, data: dict):
    df = pd.DataFrame([data])[FEATURES]
    prediction = model.predict(df)[0]   # -1 = anomaly, 1 = normal
    return prediction == -1               