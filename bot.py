import telebot
import yt_dlp

TOKEN = "8590418228:AAFKD03QvZi0bSrZ6-4dervFfCYfoEfZNck"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "ارسل رابط الفيديو من السوشل ميديا وسيتم تحميله 📥")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text

    bot.reply_to(message, "جاري تحميل الفيديو ⏳")

    ydl_opts = {'outtmpl': 'video.%(ext)s'}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        video = open(filename, 'rb')
        bot.send_video(message.chat.id, video)

    except:
        bot.reply_to(message, "لم استطع تحميل الفيديو")

bot.polling()