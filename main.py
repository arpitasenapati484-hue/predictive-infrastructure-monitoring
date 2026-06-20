from collector.metrics import collect_metrics
from storage.store import save_to_csv
from ml.anomaly import train_model, detect_anomaly
from alerts.email_alert import send_email_alert
import time, os, joblib
from config import COLLECTION_INTERVAL_SEC, ANOMALY_MODEL_PATH

model = None
if os.path.exists(ANOMALY_MODEL_PATH):
    model = joblib.load(ANOMALY_MODEL_PATH)

if __name__ == "__main__":
    count = 0
    while True:
        data = collect_metrics()
        save_to_csv(data)
        count += 1
        print("Logged:", data)

        if count == 20:  # retrain once you have some data
            model = train_model()
            print("Model trained!")

        if model and detect_anomaly(model, data):
            print("⚠️ Anomaly detected:", data)
            # send_email_alert(...) — we'll wire real credentials in later

        time.sleep(COLLECTION_INTERVAL_SEC)           