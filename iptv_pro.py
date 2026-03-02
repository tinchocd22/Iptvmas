from flask import Flask, Response
import requests
import os

app = Flask(__name__)

STREAM_URL = "https://yce5o.envivoslatam.org/espnpremium/tracks-v1a1/mono.m3u8"

@app.route("/espn")
def espn():

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://envivoslatam.org/",
        "Origin": "https://envivoslatam.org"
    }

    r = requests.get(STREAM_URL, headers=headers, stream=True)

    return Response(
        r.iter_content(chunk_size=8192),
        content_type="application/vnd.apple.mpegurl"
    )

@app.route("/")
def home():
    return "IPTV Online"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)