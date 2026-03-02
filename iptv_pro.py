from flask import Flask, Response
import requests
import os

app = Flask(__name__)

PAGE_URL = "https://nowfutbol.xyz/vivo/?c=Superliga+Argentina&o=2"   # página donde está el player
STREAM_URL = "https://smjt9q.envivoslatam.org/espnpremium/tracks-v1a1/mono.m3u8?ip=152.168.46.113&token=3bc481a33d55b1a08a83aed779702d5cdeb13e0c-5f-1772503483-1772449483"  # el m3u8 que viste en network

session = requests.Session()

@app.route("/espn")
def espn():

    headers_page = {
        "User-Agent": "Mozilla/5.0"
    }

    # 1️⃣ visitar página (activa cookies)
    session.get(PAGE_URL, headers=headers_page)

    headers_stream = {
        "User-Agent": "Mozilla/5.0",
        "Referer": PAGE_URL,
        "Origin": "https://envivoslatam.org"
    }

    # 2️⃣ pedir stream con cookies activas
    r = session.get(STREAM_URL, headers=headers_stream, stream=True)

    return Response(
        r.iter_content(chunk_size=8192),
        content_type=r.headers.get("Content-Type", "application/vnd.apple.mpegurl")
    )


@app.route("/")
def home():
    return "IPTV Online"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)