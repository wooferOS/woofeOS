from flask import Flask, request
import telebot
import openai
import logging
import time

# 🔐 Ключі
TOKEN = "7778803208:AAEe8SM8Fd7nbQ8H8AdJeLQjUqlnWAlW2K0"
OPENAI_API_KEY = "🧠_GPT_KEY_СЮДИ_ДОДАЙ_В_ENV"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
openai.api_key = OPENAI_API_KEY

# 🔧 Таймаут
telebot.apihelper.READ_TIMEOUT = 5
telebot.apihelper.CONNECT_TIMEOUT = 3

# 📜 Логування
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["POST", "GET"])
def webhook():
    if request.method == "POST":
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return "ok", 200
    return "👋 I'm alive", 200

# 📍 /start
@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "👋 Привіт! Я Woofer SMM Bot — готовий допомогти з TikTok 🎬")

# 🆘 /help
@bot.message_handler(commands=["help"])
def handle_help(message):
    commands = "/start /help /ping /report /today"
    bot.send_message(message.chat.id, f"🧩 Команди доступні:\n{commands}")

# 📶 /ping
@bot.message_handler(commands=["ping"])
def handle_ping(message):
    bot.send_message(message.chat.id, "🏓 pong")

# 📊 /report
@bot.message_handler(commands=["report"])
def handle_report(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": "Придумай абсурдну ідею для SMM TikTok із собаками-кухарями"
            }],
            timeout=10
        )
        text = response.choices[0].message.content.strip()
        bot.send_message(message.chat.id, f"🐾 Ідея: {text}")
    except Exception as e:
        logging.error(f"GPT error: {e}")
        bot.send_message(message.chat.id, "🚫 Помилка при зверненні до GPT")

# 💬 Загальні запити до GPT
@bot.message_handler(func=lambda message: True)
def handle_gpt_chat(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message.text}],
            timeout=10
        )
        reply = response.choices[0].message.content.strip()
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        logging.error(f"GPT error: {e}")
        bot.send_message(message.chat.id, "⚠️ GPT не відповідає. Спробуй ще раз.")

# 🧠 Примітка
# Всі секрети зберігай у Render > Environment:
# - TELEGRAM_API_TOKEN
# - OPENAI_API_KEY
