import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Переменные окружения (будем заполнять в Railway)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_to_telegram(message):
    """Функция отправки сообщения в Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

@app.route("/youtube", methods=["POST"])
def youtube_webhook():
    """Обрабатываем уведомления от YouTube"""
    data = request.data.decode("utf-8")
    if "yt:videoId" in data:
        video_id = data.split("yt:videoId>")[1].split("</")[0]
        send_to_telegram(f"🔴 Начался стрим! https://www.youtube.com/watch?v={video_id}")
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "YouTube Webhook is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))