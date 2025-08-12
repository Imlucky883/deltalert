import os
import json
import asyncio
import websockets
import argparse
from plyer import notification
from dotenv import load_dotenv
from datetime import datetime

def get_args():
    parser = argparse.ArgumentParser(description="Crypto WebSocket Client")
    parser.add_argument("--exchange", type=str, default="delta", help="Exchange name (delta/binance)")
    parser.add_argument("--symbol", type=str, default="BTCUSD", help="Trading pair symbol")
    parser.add_argument("--interval", type=str, default="1m", help="Candle interval")
    parser.add_argument("--target-high", type=float, help="Target high price")
    parser.add_argument("--target-low", type=float, default=None, help="Target low price")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()

args = get_args()

# Load alerts from JSON file
alerts = []
if os.path.exists("alerts.json"):
    with open("alerts.json") as f:
        alerts = json.load(f)

triggered_alerts = set()  # To prevent repeated triggers

# Load env variables
load_dotenv()

TARGET_HIGH = args.target_high if args.target_high is not None else float(os.getenv("TARGET_HIGH", 0))
TARGET_LOW = args.target_low if args.target_low is not None else float(os.getenv("TARGET_LOW", 0))
SYMBOL = args.symbol or os.getenv("SYMBOL", "BTCUSD")

WS_URL = "wss://socket.delta.exchange"

async def price_alert():
    async with websockets.connect(WS_URL) as ws:
        # Subscribe to ticker for given symbol
        subscribed_symbols = list({SYMBOL} | {a["symbol"] for a in alerts})
        subscribe_message = {
            "type": "subscribe",
            "payload": {
                "channels": [
                    {
                        "name": "v2/ticker",
                        "symbols": subscribed_symbols
                    }
                ]
            }
        }
        await ws.send(json.dumps(subscribe_message))
        print(f"Subscribed to {', '.join(subscribed_symbols)} ticker. Waiting for price updates...")

        async for message in ws:
            data = json.loads(message)

            # Filter ticker data
            if data.get("type") == "v2/ticker":
                symbol = data["symbol"]
                mark_price = float(data["mark_price"])
                print(f"{symbol} price: {mark_price}")

                # ----CLI/ENV alerts-------
                if symbol == SYMBOL:
                    if TARGET_HIGH and mark_price >= TARGET_HIGH:
                        send_alert(f"High target hit: {mark_price} >= {TARGET_HIGH}")
                    if TARGET_LOW and mark_price <= TARGET_LOW:
                        send_alert(f"Low target hit: {mark_price} <= {TARGET_LOW}")
              
                for alert in alerts:
                    key = (alert["symbol"], alert["type"], alert["value"])
                    if key in triggered_alerts:
                        continue

                    if alert["symbol"] == symbol:
                        if alert["type"] == "gte" and mark_price >= alert["value"]:
                            send_alert(f"[JSON] {symbol} >= {alert['value']} (Current: {mark_price})", symbol)
                            triggered_alerts.add(key)
                            alerts.remove[alert]
                        elif alert["type"] == "lte" and mark_price <= alert["value"]:
                            send_alert(f"[JSON] {symbol} <= {alert['value']} (Current: {mark_price})", symbol)
                            triggered_alerts.add(key)
                            alerts.remove[alert]

 
def send_alert(message,symbol):
    """Send desktop notification and log to file."""
    notification.notify(
        title="Price Alert",
        message=message,
        timeout=5
    )
    log_alert(message,symbol)
    print(message)

def log_alert(message,symbol):
    """Append alert message to alerts.log with timestamp."""
    with open("alerts.log", "a") as f:
        f.write(f"{datetime.now()} - {symbol} - {message}\n")

if __name__ == "__main__":
    asyncio.run(price_alert())
