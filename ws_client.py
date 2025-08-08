
import os
import json
import asyncio
import websockets
from plyer import notification
from dotenv import load_dotenv

# Load env variables
load_dotenv()
TARGET_PRICE = float(os.getenv("TARGET_PRICE", 0))
SYMBOL = os.getenv("SYMBOL", "BTCUSD")

WS_URL = "wss://socket.delta.exchange"

async def price_alert():
    async with websockets.connect(WS_URL) as ws:
        # Subscribe to ticker for given symbol
        subscribe_message = {
            "type": "subscribe",
            "payload": {
                "channels": [
                    {
                        "name": "v2/ticker",
                        "symbols": [SYMBOL]
                    }
                ]
            }
        }
        await ws.send(json.dumps(subscribe_message))
        print(f"Subscribed to {SYMBOL} ticker. Waiting for price updates...")

        async for message in ws:
            data = json.loads(message)

            # Filter ticker data
            if data.get("type") == "v2/ticker":
                mark_price = float(data["mark_price"])
                print(f"{SYMBOL} price: {mark_price}")

                if mark_price >= TARGET_PRICE:
                    notification.notify(
                        title=f"{SYMBOL} Alert",
                        message=f"Price hit {mark_price}!",
                        timeout=5
                    )
                    print(f"Target hit: {mark_price} >= {TARGET_PRICE}")
                    return  # Exit after first alert

if __name__ == "__main__":
    asyncio.run(price_alert())
