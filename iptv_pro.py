from flask import Flask, Response
import requests
import os

app = Flask(__name__)

# ⚠️ PONÉ TU M3U8 REAL AQUÍ
STREAM_URL = "https://pvtn5y.envivoslatam.org/espnpremium/tracks-v1a1/mono.m3u8"

# ------------------------------------------------
# PROXY STREAM (SIN NAVEGADOR)
# ------------------------------------------------
@app.route("/espn")
def espn():

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://envivoslatam.org/"
    }

    r = requests.get(STREAM_URL, headers=headers, stream=True)

    return Response(
        r.iter_content(chunk_size=1024),
        content_type="application/vnd.apple.mpegurl"
    )

# ------------------------------------------------
@app.route("/")
def home():
    return "IPTV Online"

# ------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)