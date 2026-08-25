import os

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")

def home():

    return """

    <!DOCTYPE html>

    <html lang="uk">

    <head>

        <meta charset="UTF-8">

        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>OTC Signal Pro</title>

        <style>

            body {

                background: #0b1020;

                color: white;

                font-family: Arial, sans-serif;

                text-align: center;

                padding: 40px 20px;

            }

            .card {

                max-width: 500px;

                margin: auto;

                background: #151c30;

                padding: 30px;

                border-radius: 20px;

            }

            h1 {

                margin-bottom: 10px;

            }

            .status {

                color: #55e6a5;

                font-weight: bold;

            }

        </style>

    </head>

    <body>

        <div class="card">

            <h1>OTC Signal Pro</h1>

            <p>Trading Signal Dashboard</p>

            <p class="status">● SYSTEM ONLINE</p>

            <p>Application successfully deployed.</p>

        </div>

    </body>

    </html>

    """

@app.route("/health")

def health():

    return jsonify({

        "status": "ok",

        "app": "OTC Signal Pro"

    })

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(host="0.0.0.0", port=port)
