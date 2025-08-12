import asyncio
import json
import websockets
import os
from config import WS_URL
from alerts import load_alerts, remove_alert
from notifications import send_desktop_alert, send_email, build_email_body
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")

triggered_alerts = set()

async def price_alert():
    alerts = load_alerts()
    subscribed_symbols = list({a["symbol"] for a in alerts})
    
    async with websockets.connect(WS_URL) as ws:
        subscribe_message = {
            "type": "subscribe",
            "payload": {
                "channels": [
                    {
                        "name": "v2/ticker",
                        "symbols": "all"
                    }
                ]
            }
        }
        await ws.send(json.dumps(subscribe_message))
        print(f"Subscribed to {', '.join(subscribed_symbols)} ticker. Waiting for price updates...")

        async for message in ws:
            data = json.loads(message)

            if data.get("type") == "v2/ticker":
                symbol = data["symbol"]
                mark_price = float(data["mark_price"])
                print(f"{symbol} price: {mark_price}")

                # JSON alerts
                for alert in alerts.copy():  # iterate over a copy since we may remove
                    if alert["symbol"] == symbol:
                        condition_met = (
                            (alert["type"] == "gte" and mark_price >= alert["value"]) or
                            (alert["type"] == "lte" and mark_price <= alert["value"])
                        )
                        if condition_met:
                            comp = ">=" if alert["type"] == "gte" else "<="
                            send_desktop_alert(f"[JSON] {symbol} {comp} {alert['value']} (Current: {mark_price})", symbol)
                            body = build_email_body(symbol, alert["type"], alert["value"], mark_price)
                            send_email(f"Alert Triggered for {symbol}", body, EMAIL_USER)
                            remove_alert(alert, alerts)
if __name__ == "__main__":
    asyncio.run(price_alert())
