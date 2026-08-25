import os

import random

import requests

from datetime import datetime, timedelta

from zoneinfo import ZoneInfo

from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

BASE_URL = "https://otc-signal-pro.onrender.com"

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

TIMEZONE = ZoneInfo("Europe/Rome")

PAIRS = [

    "EUR/USD OTC",

    "GBP/USD OTC",

    "USD/JPY OTC",

    "AUD/USD OTC",

    "EUR/GBP OTC",

]

def send_message(chat_id, text):

    requests.post(

        f"{TELEGRAM_API}/sendMessage",

        json={

            "chat_id": chat_id,

            "text": text,

            "parse_mode": "HTML"

        },

        timeout=15

    )

def next_entry_time():

    now = datetime.now(TIMEZONE)

    # Сигнал приблизно на 2 хвилини вперед

    entry = now + timedelta(minutes=2)

    # Вхід завжди рівно на 30-й секунді

    entry = entry.replace(second=30, microsecond=0)

    return entry

def create_demo_signal():

    now = datetime.now(TIMEZONE)

    entry = next_entry_time()

    pair = random.choice(PAIRS)

    direction = random.choice(["UP", "DOWN"])

    if direction == "UP":

        direction_text = "🟢 UP ⬆️"

    else:

        direction_text = "🔴 DOWN ⬇️"

    return (

        "🚨 <b>OTC SIGNAL — DEMO</b>\n\n"

        f"💱 <b>{pair}</b>\n"

        f"{direction_text}\n\n"

        f"📨 Signal time: {now.strftime('%H:%M:%S')}\n"

        f"🎯 <b>ENTRY: {entry.strftime('%H:%M:%S')}</b>\n"

        "⏱ <b>S3</b>\n"

        "⌛ <b>Expiration: 3 sec</b>\n\n"

        "⏳ Сигнал надіслано завчасно.\n"

        "⚠️ DEMO: UP/DOWN поки вибирається випадково."

    )

@app.route("/")

def home():

    return "OTC Signal Pro is ONLINE"

@app.route("/setup")

def setup_webhook():

    if not BOT_TOKEN:

        return jsonify({

            "ok": False,

            "error": "TELEGRAM_BOT_TOKEN is missing"

        })

    response = requests.post(

        f"{TELEGRAM_API}/setWebhook",

        json={

            "url": f"{BASE_URL}/telegram"

        },

        timeout=15

    )

    return response.json()

@app.route("/telegram", methods=["POST"])

def telegram_webhook():

    data = request.get_json(silent=True) or {}

    message = data.get("message")

    if not message:

        return jsonify({"ok": True})

    chat_id = message["chat"]["id"]

    text = message.get("text", "").strip()

    if text == "/start":

        send_message(

            chat_id,

            "🤖 <b>OTC SIGNAL PRO</b>\n\n"

            "✅ Bot connected\n"

            "📊 Mode: DEMO\n\n"

            "🎯 Entry: приблизно через 2 хвилини\n"

            "🕐 Entry second: :30\n"

            "⏱ Expiration: 3 sec (S3)\n\n"

            "Команди:\n"

            "/signal — отримати тестовий сигнал\n"

            "/status — перевірити статус"

        )

    elif text == "/signal":

        send_message(

            chat_id,

            create_demo_signal()

        )

    elif text == "/status":

        now = datetime.now(TIMEZONE)

        send_message(

            chat_id,

            "✅ <b>OTC Signal Pro ONLINE</b>\n\n"

            f"🕐 Current time: {now.strftime('%H:%M:%S')}\n"

            "📊 Mode: DEMO\n"

            "🎯 Entry timing: :30\n"

            "⏱ Expiration: 3 sec\n"

            "⏳ Warning: ~2 minutes before entry"

        )

    else:

        send_message(

            chat_id,

            "Команди:\n"

            "/start\n"

            "/signal\n"

            "/status"

        )

    return jsonify({"ok": True})

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(

        host="0.0.0.0",

        port=port

    )
