
import os
import json

ALERTS_FILE = "alerts.json"

def load_alerts():
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE) as f:
            return json.load(f)
    return []

def save_alerts(alerts):
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=4)

def remove_alert(alert, alerts):
    if alert in alerts:
        alerts.remove(alert)
        save_alerts(alerts)
