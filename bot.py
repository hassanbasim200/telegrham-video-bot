import telebot
import yt_dlp
import os
from flask import Flask
from threading import Thread

TOKEN = "8662573579:AAFMuw8BTZXPvlqcVqsivFXBfT1z5uXPmXQ"

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text

    bot.reply_to(message, "جاري التحميل...")

    try:
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': 'video.mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open("video.mp4", "rb") as video:
            bot.send_document(message.chat.id, video)

        os.remove("video.mp4")

    except Exception as e:
        bot.reply_to(message, str(e))

keep_alive()

print("Bot Running")

bot.infinity_polling()
