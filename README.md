
# Deltalert

A lightweight Python script to monitor live cryptocurrency prices (e.g., BTC, ETH) from a WebSocket feed and trigger alerts when prices cross your configured thresholds.  
Supports **desktop notifications** and **email alerts** for maximum flexibility.

---

## 🚀 Features

- **Live WebSocket price tracking** (e.g., Binance stream)
- **Custom alerts per cryptocurrency** via `alerts.json`
- **Desktop notifications** (instant pop-ups)
- **Email alerts** (with custom subject & body)
- **Auto-remove triggered alerts** (one-time alert behavior)
- **Lightweight & easy to deploy**

---

## 📂 Project Structure
```plaintext
deltalert/
├── alerts.json         # Stores your alerts for different pairs
├── alerts.log          # Stores triggered alerts
├── config.py           # Config values (WebSocket URL)
├── ws_client.py        # Main WebSocket client script
├── alerts.py           # Functions to load & manage alerts
├── notifications.py    # Functions to send desktop/email alerts
├── requirements.txt    # Dependencies
├── README.md           # Documentation
└── .env                # Environment variables (email credentials)
```

---

## ⚙️ Installation

**1️⃣ Clone the repository:**
```bash
git clone https://github.com/Imlucky883/deltalert.git
cd deltalert
```

2️⃣ Create a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

3️⃣ Install dependencies:
```python
pip install -r requirements.txt
```

4️⃣ Configure `.env` for email alerts:
```
EMAIL_USER=your_email@example.com
EMAIL_PASSWORD=your_email_password
```
5️⃣ Run the alert service
```bash
python ws_client.py
```

---

## 📸 Example Output

![output.png](/assets/output.png)
