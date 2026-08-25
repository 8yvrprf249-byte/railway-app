import os

import requests

from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

BASE_URL = "https://otc-signal-pro.onrender.com"

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

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

    webhook_url = f"{BASE_URL}/telegram"

    response = requests.post(

        f"{TELEGRAM_API}/setWebhook",

        json={"url": webhook_url},

        timeout=15

    )

    return response.json()

@app.route("/telegram", methods=["POST"])

def telegram_webhook():

    data = request.get_json(silent=True) or {}

    message = data.get("message")

    if message:

        chat_id = message["chat"]["id"]

        text = message.get("text", "")

        if text == "/start":

            send_message(

                chat_id,

                "🤖 <b>OTC SIGNAL PRO</b>\n\n"

                "✅ Bot connected\n"

                "📊 Signal system: DEMO\n\n"

                "💱 EUR/USD OTC\n"

                "🟢 UP ⬆️\n"

                "⏱ M1\n"

                "🎯 ENTRY: 15:42:30\n\n"

                "⚠️ Test mode."

            )

        elif text == "/test":

            send_message(

                chat_id,

                "🚨 <b>OTC SIGNAL</b>\n\n"

                "💱 EUR/USD OTC\n"

                "🟢 UP ⬆️\n"

                "⏱ M1\n"

                "🎯 ENTRY: 15:42:30\n"

                "⌛ Expiration: 5 sec\n\n"

                "🧪 TEST SIGNAL"

            )

        else:

            send_message(

                chat_id,

                "OTC Signal Pro is online.\n"

                "Use /start or /test."

            )

    return jsonify({"ok": True})

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(host="0.0.0.0", port=port)
