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
    print("🚀 Predictive Infrastructure Monitor starting...")
    while True:
        data = collect_metrics()

        if data is None:
            print("⚠️ Skipping this cycle due to collector error.")
            time.sleep(COLLECTION_INTERVAL_SEC)
            continue

        save_to_csv(data)
        count += 1
        print(f"[{count}] Logged: CPU={data['cpu_percent']}% RAM={data['ram_percent']}% Disk={data['disk_percent']}%")

        if count == 20:
            model = train_model()
            print("✅ Model trained!")

        if model and detect_anomaly(model, data):
            print("🚨 Anomaly detected!", data)

        time.sleep(COLLECTION_INTERVAL_SEC)