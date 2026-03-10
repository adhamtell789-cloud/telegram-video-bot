import telebot
import yt_dlp
import os
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN)

# رسالة البداية
@bot.message_handler(commands=['start'])
def start(message):

    text = (
        "👋 مرحباً بك في بوت تحميل الفيديو\n\n"
        "أرسل رابط فيديو من:\n\n"
        "• TikTok\n"
        "• Instagram\n"
        "• YouTube\n"
        "• Facebook\n"
        "• Twitter / X\n\n"
        "وسأقوم بتحميله لك فوراً 📥"
    )

    bot.reply_to(message, text)


# تحميل الفيديو
@bot.message_handler(func=lambda message: True)
def download_video(message):

    url = message.text

    msg = bot.reply_to(message, "⏳ جاري تحميل الفيديو...")

    ydl_opts = {
        'format': 'best[ext=mp4][height<=720]',
        'outtmpl': 'video.%(ext)s',
        'noplaylist': True,
        'quiet': True
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        bot.edit_message_text(
            "📤 جاري إرسال الفيديو...",
            message.chat.id,
            msg.message_id
        )

        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(filename)

    except Exception as e:

        bot.edit_message_text(
            "❌ لم أستطع تحميل هذا الرابط.\n"
            "تأكد أن الرابط صحيح.",
            message.chat.id,
            msg.message_id
        )


# إبقاء السيرفر يعمل
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"


def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


def keep_alive():
    t = Thread(target=run)
    t.start()


keep_alive()

bot.infinity_polling()

        
