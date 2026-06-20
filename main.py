from collector.metrics import collect_metrics
from storage.store import save_to_csv
import time
from config import COLLECTION_INTERVAL_SEC

if __name__ == "__main__":
    while True:
        data = collect_metrics()
        save_to_csv(data)
        print("Logged:", data)
        time.sleep(COLLECTION_INTERVAL_SEC)