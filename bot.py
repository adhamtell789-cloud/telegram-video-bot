import telebot
import yt_dlp
import os
from flask import Flask
from threading import Thread

TOKEN = "8590418228:AAFKD03QvZi0bSrZ6-4dervFfCYfoEfZNck"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
    "👋 مرحباً!\n\n"
    "أرسل رابط الفيديو أو الريلز أو المنشور وسأقوم بتحميله لك.\n\n"
    "المواقع المدعومة:\n"
    "TikTok\nInstagram\nYouTube\nFacebook\nTwitter")

@bot.message_handler(func=lambda message: True)
def download_video(message):

    url = message.text

    bot.reply_to(message,"⏳ جاري تحميل الفيديو...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'noplaylist': True
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename,'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(filename)

    except Exception as e:
        bot.reply_to(message,"❌ لم أستطع تحميل هذا الرابط.")

# -------- حل مشكلة Render --------

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run():
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

bot.infinity_polling()