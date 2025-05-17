from flask import Flask, request
import telebot
import os
import openai
import logging

# Логування
logging.basicConfig(level=logging.INFO)

# Змінні середовища
TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
openai.api_key = OPENAI_API_KEY

# Вебхук
@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

# /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привіт! Я Woofer Bot — TikTok SMM помічник 🐶")

# /help
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "/start /help /ping /report /today — Просто напиши щось, і я відповім!")

# /ping
@bot.message_handler(commands=['ping'])
def ping_message(message):
    bot.send_message(message.chat.id, "pong 🏓")

# /report
@bot.message_handler(commands=['report'])
def report_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Придумай щось смішне або абсурдне для TikTok з песиками-кухарями"}],
            timeout=15  # таймаут
        )
        reply = response.choices[0].message.content
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        logging.error(f"GPT помилка: {e}")
        bot.send_message(message.chat.id, "GPT помилка 😢")

# Відповідь на будь-яке інше повідомлення
@bot.message_handler(func=lambda message: True)
def gpt_chat(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message.text}],
            timeout=15
        )
        reply = response.choices[0].message.content
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        logging.error(f"GPT помилка: {e}")
        bot.send_message(message.chat.id, "GPT помилка 😢")
