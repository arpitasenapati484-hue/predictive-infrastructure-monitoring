import urllib.request
import json

def send_telegram_alert(message: str, bot_token: str, chat_id: str):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": message}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            print("Telegram alert sent!")
            return response.read()
    except Exception as e:
        print(f"Telegram alert failed: {e}")