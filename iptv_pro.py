from flask import Flask, redirect
from playwright.sync_api import sync_playwright
import time
import os

app = Flask(__name__)

WEB_URL = "https://nowfutbol.xyz/vivo/?c=Superliga+Argentina&o=2"

# ===== CACHE =====
cache_stream = None
cache_time = 0
CACHE_DURACION = 300  # 5 minutos


# ==============================
# OBTENER STREAM REAL
# ==============================
def obtener_stream_real():
    print("🔎 Buscando nuevo stream...")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu"
                ]
            )

            page = browser.new_page()
            stream_url = None

            def capturar(response):
                nonlocal stream_url
                if ".m3u8" in response.url:
                    stream_url = response.url
                    print("🎯 Stream encontrado:", stream_url)

            page.on("response", capturar)

            page.goto(WEB_URL, timeout=60000)
            page.wait_for_timeout(5000)

            # 🔎 Ver si hay iframe
            frames = page.frames
            print("Frames encontrados:", len(frames))

            for frame in frames:
                try:
                    frame.click("video", timeout=2000)
                except:
                    pass
                try:
                    frame.click("button", timeout=2000)
                except:
                    pass

            # También intentar en página principal
            try:
                page.click("video", timeout=2000)
            except:
                pass

            page.wait_for_timeout(10000)

            browser.close()

            return stream_url

    except Exception as e:
        print("❌ Error Playwright:", e)
        return None


# ==============================
# CACHE
# ==============================
def obtener_stream_cache():
    global cache_stream, cache_time

    ahora = time.time()

    if cache_stream and (ahora - cache_time < CACHE_DURACION):
        print("⚡ Usando cache")
        return cache_stream

    nuevo = obtener_stream_real()

    if nuevo:
        cache_stream = nuevo
        cache_time = ahora

    return cache_stream


# ==============================
# RUTAS
# ==============================
@app.route("/espn")
def espn():
    link = obtener_stream_cache()

    if not link:
        return "Canal offline ❌"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": WEB_URL
    }

    r = requests.get(link, headers=headers)

    return Response(r.content, content_type="application/vnd.apple.mpegurl")


@app.route("/espn")
def espn():
    link = obtener_stream_cache()

    if link:
        return redirect(link)
    import requests
from flask import Response

    return "Canal offline ❌"


# ==============================
# SOLO PARA LOCAL
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)