
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

# Час Італії

TIMEZONE = ZoneInfo("Europe/Rome")

# DEMO-пари

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

    """

    Вибираємо майбутній момент входу на :30.

    Даємо щонайменше ~45 секунд на підготовку.

    """

    now = datetime.now(TIMEZONE)

    entry = now.replace(second=30, microsecond=0)

    if entry <= now + timedelta(seconds=45):

        entry += timedelta(minutes=1)

    return entry

def create_demo_signal():

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

        f"{direction_text}\n"

        "⏱ M1\n"

        f"🎯 <b>ENTRY: {entry.strftime('%H:%M:%S')}</b>\n"

        "⌛ Expiration: 5 sec\n\n"

        "⚠️ DEMO: UP/DOWN зараз вибирається випадково.\n"

        "Не використовуй цей сигнал для реальної ставки."

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

        json={"url": f"{BASE_URL}/telegram"},

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

            "✅ Bot connected\n\n"

            "Команди:\n"

            "/signal — тестовий OTC-сигнал\n"

            "/status — статус бота\n\n"

            "⚠️ Зараз працюємо в DEMO."

        )

    elif text == "/signal":

        send_message(chat_id, create_demo_signal())

    elif text == "/status":

        now = datetime.now(TIMEZONE)

        send_message(

            chat_id,

            "✅ <b>OTC Signal Pro ONLINE</b>\n\n"

            f"🕐 {now.strftime('%H:%M:%S')}\n"

            "📊 Mode: DEMO\n"

            "🎯 Entry timing: :30"

        )

    else:

        send_message(

            chat_id,

            "Команди:\n"

            "/signal\n"

            "/status"

        )

    return jsonify({"ok": True})

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(host="0.0.0.0", port=port)
