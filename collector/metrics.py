import psutil
import time

def collect_metrics():
    try:
        return {
            "timestamp": time.time(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "ram_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "net_sent": psutil.net_io_counters().bytes_sent,
            "net_recv": psutil.net_io_counters().bytes_recv,
        }
    except Exception as e:
        print("Collector error:", e)
        return None

if __name__ == "__main__":
    print(collect_metrics())