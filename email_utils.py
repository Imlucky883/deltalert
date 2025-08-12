
# email_utils.py
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv 
import config

load_dotenv()

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = config.EMAIL_ADDRESS
    msg["To"] = to_email

    with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
