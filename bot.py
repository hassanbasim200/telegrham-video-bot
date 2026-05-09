import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8662573579:AAFMuw8BTZXPvlqcVqsivFXBfT1z5uXPmXQ"

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "x.com" not in url and "twitter.com" not in url:
        await update.message.reply_text("ارسل رابط X صحيح")
        return

    await update.message.reply_text("جاري التحميل...")

    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video."):
                await update.message.reply_video(video=open(file, 'rb'))
                os.remove(file)
                break

    except Exception as e:
        await update.message.reply_text(f"خطأ: {e}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

print("Bot Running...")
app.run_polling()
