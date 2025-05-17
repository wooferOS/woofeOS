from flask import Flask, request
import telebot
import openai
import os
import logging

# 🔐 Безпечне підключення до ключів
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_API_TOKEN)
openai.api_key = OPENAI_API_KEY
app = Flask(__name__)

# ⏱ Таймаути
telebot.apihelper.READ_TIMEOUT = 5
telebot.apihelper.CONNECT_TIMEOUT = 3

# 🧾 Логування
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "ok", 200
    return "✅ Woofer bot is live", 200

# 🟢 /start
@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.send_message(message.chat.id, "🐶 Привіт! Я — Woofer SMM Bot. Готовий працювати над TikTok 🎬")

# 🧠 /help
@bot.message_handler(commands=["help"])
def help_handler(message):
    bot.send_message(message.chat.id,
                     "🛠 Команди:\n"
                     "/start — запуск\n"
                     "/help — допомога\n"
                     "/ping — перевірка\n"
                     "/report — ідея для TikTok\n"
                     "Напиши будь-що — я відповім як GPT 🧠")

# 🛰 /ping
@bot.message_handler(commands=["ping"])
def ping_handler(message):
    bot.send_message(message.chat.id, "🏓 pong")

# 🧪 /report
@bot.message_handler(commands=["report"])
def report_handler(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": "Придумай абсурдну ідею для TikTok з собаками-кухарями"
            }],
            timeout=10
        )
        reply = response.choices[0].message.content.strip()
        bot.send_message(message.chat.id, f"🔥 Ідея для TikTok:\n{reply}")
    except Exception as e:
        logging.error(f"GPT error: {e}")
        bot.send_message(message.chat.id, "🚫 Помилка генерації ідеї. GPT не відповів.")

# 💬 Відповідь GPT на будь-яке повідомлення
@bot.message_handler(func=lambda message: True)
def gpt_chat_handler(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": message.text
            }],
            timeout=10
        )
        reply = response.choices[0].message.content.strip()
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        logging.error(f"GPT error: {e}")
        bot.send_message(message.chat.id, "⚠️ Щось пішло не так. Спробуй пізніше.")
