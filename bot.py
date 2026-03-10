import os
import time
import json
import yt_dlp
import telebot

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

ADMIN_ID = 8273617578

USERS_FILE = "users.json"
COOLDOWN = {}

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

def load_users():
    with open(USERS_FILE) as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def add_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)

@bot.message_handler(commands=['start'])
def start(message):

    add_user(message.from_user.id)

    text = """
👋 مرحباً بك في بوت تحميل الفيديوهات

📥 أرسل رابط فيديو من:

• TikTok
• Instagram
• Facebook
• Twitter
• YouTube

وسيتم تحميله بدون علامة مائية.
"""

    bot.reply_to(message, text)

@bot.message_handler(commands=['stats'])
def stats(message):

    if message.from_user.id != ADMIN_ID:
        return

    users = load_users()

    bot.send_message(
        message.chat.id,
        f"📊 عدد مستخدمي البوت: {len(users)}"
    )

@bot.message_handler(commands=['broadcast'])
def broadcast(message):

    if message.from_user.id != ADMIN_ID:
        return

    text = message.text.replace("/broadcast ", "")

    users = load_users()

    sent = 0

    for user in users:

        try:
            bot.send_message(user, text)
            sent += 1
        except:
            pass

    bot.send_message(message.chat.id, f"✅ تم الإرسال إلى {sent}")

def download_video(url):

    ydl_opts = {
        "format": "best",
        "outtmpl": "video.%(ext)s",
        "noplaylist": True,
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@bot.message_handler(func=lambda m: "http" in m.text)
def handle_link(message):

    user_id = message.from_user.id

    if user_id in COOLDOWN and time.time() - COOLDOWN[user_id] < 8:
        bot.reply_to(message, "⏳ انتظر قليلاً قبل إرسال رابط آخر")
        return

    COOLDOWN[user_id] = time.time()

    url = message.text

    msg = bot.reply_to(message, "⏳ جاري تحميل الفيديو...")

    try:

        file = download_video(url)

        with open(file, "rb") as video:
            bot.send_video(message.chat.id, video)

        os.remove(file)

        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:

        bot.reply_to(message, "❌ لم أستطع تحميل الفيديو")

while True:

    try:

        print("Bot running...")

        bot.infinity_polling(timeout=60, long_polling_timeout=60)

    except Exception as e:

        print("Error:", e)

        time.sleep(5)
