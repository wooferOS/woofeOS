import os
from flask import Flask, request
import telebot
import openai
import random

# Ініціалізація
TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
openai.api_key = OPENAI_KEY

# Webhook
@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

# Команди
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привіт! Я Woofer Bot — допоможу з TikTok 🌭")

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "/start /help /ping /today /report")

@bot.message_handler(commands=['ping'])
def ping_message(message):
    bot.send_message(message.chat.id, "pong 🏓")

@bot.message_handler(commands=['report'])
def report_message(message):
    ideas = [
        "🐶 Цуценята сьогодні танцювали в стилі хіп-хоп!",
        "🎥 Нове відео: як зробити бургер із хвостиком!",
        "📊 Тренд тижня: більше кетчупу = більше переглядів.",
        "🎭 Час для пародії на Gordon Ramsay, але з цуценятами!"
    ]
    bot.send_message(message.chat.id, random.choice(ideas))

# GPT-відповіді
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти веселий пес-кухар із TikTok, відповідай креативно та коротко."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message.content.strip()
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, "Вибач, щось не так. 🐾")
