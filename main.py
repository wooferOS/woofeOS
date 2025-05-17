import telebot
from telebot import types
from flask import Flask, request
import openai
import os
import traceback

# Ініціалізація токенів
BOT_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PORT = int(os.environ.get("PORT", 5000))

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Налаштування нового клієнта OpenAI
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Обробка команди /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привіт! Я Woofer Bot — TikTok SMM помічник 🐶")

# Обробка команди /help
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "/start /help /ping /report /today — Просто напиши щось, і я відповім!")

# Обробка команди /ping
@bot.message_handler(commands=['ping'])
def ping_message(message):
    bot.send_message(message.chat.id, "Pong! 🏓")

# Обробка команди /report з GPT
@bot.message_handler(commands=['report'])
def report_message(message):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ти SMM-помічник TikTok сторінки з песиками-кухарями."},
                {"role": "user", "content": "Зроби короткий SMM-звіт за сьогодні з гумором і стильно 🐶🍔"},
            ]
        )
        reply = response.choices[0].message.content
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        print("❌ GPT помилка:", e)
        print(traceback.format_exc())
        bot.send_message(message.chat.id, "GPT помилка 😢")

# Обробка команди /today
@bot.message_handler(commands=['today'])
def today_message(message):
    bot.send_message(message.chat.id, "Сьогодні в TikTok: 3 пости, 2 коментарі, 1 шалений цуцик 🐾")

# Обробка будь-якого іншого повідомлення
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Цуцик почув: " + message.text)

# Flask endpoint для Webhook
@app.route('/', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'OK'

# Запуск Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
