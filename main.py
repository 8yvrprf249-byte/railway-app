import os

import requests

from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):

    if not BOT_TOKEN:

        return

    requests.post(

        f"{TELEGRAM_API}/sendMessage",

        json={

            "chat_id": chat_id,

            "text": text,

            "parse_mode": "HTML"

        },

        timeout=10

    )

@app.route("/")

def home():

    return "OTC Signal Pro is ONLINE"

@app.route("/health")

def health():

    return jsonify({

        "status": "ok",

        "app": "OTC Signal Pro"

    })

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

                "Example signal:\n"

                "💱 EUR/USD OTC\n"

                "🟢 UP ⬆️\n"

                "⏱ M1\n"

                "🎯 ENTRY: 15:42:30\n\n"

                "⚠️ Test mode — no automatic trades."

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

                "OTC Signal Pro is online.\n\n"

                "Use /start or /test."

            )

    return jsonify({"ok": True})

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(host="0.0.0.0", port=port)
