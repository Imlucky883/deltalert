from plyer import notification
from datetime import datetime
import smtplib
import os
from email.mime.text import MIMEText
from config import SMTP_SERVER, SMTP_PORT
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_desktop_alert(message, symbol):
    notification.notify(
        title="Price Alert",
        message=message,
        timeout=5
    )
    log_alert(message, symbol)
    print(message)

def log_alert(message, symbol):
    with open("alerts.log", "a") as f:
        f.write(f"{datetime.now()} - {symbol} - {message}\n")
from datetime import datetime

def build_email_body(symbol, alert_type, target_value, current_price):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert_desc = "risen above" if alert_type == "gte" else "fallen below"
    alert_type_full = "Greater Than or Equal To" if alert_type == "gte" else "Less Than or Equal To"

    body = f"""
Hello there,

This is an automated alert from your Delta Exchange price watcher.
The trading pair {symbol} has just {alert_desc} your target price of {target_value}.
Current price: {current_price}

Please take appropriate action.

Best regards,
Delta-Bot
"""
    return body


def send_email(subject, body, to_email):
    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("Email credentials not set. Skipping email alert.")
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
