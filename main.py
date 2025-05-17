from flask import Flask, request
import telebot
import os
import openai
import logging

# Logging
logging.basicConfig(level=logging.INFO)

# Init Flask app and bot
app = Flask(__name__)
TOKEN = os.environ.get("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN, threaded=False)
openai.api_key = OPENAI_API_KEY

# Webhook endpoint
@app.route('/', methods=['POST'])
def webhook():
    try:
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
    except Exception as e:
        logging.error(f"Error in webhook: {e}")
    return "ok", 200

# Commands
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привіт! Я Woofer Bot — TikTok SMM помічник 🐶")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "/start /help /ping /report /today — Просто напиши щось, і я відповім!")

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.send_message(message.chat.id, "pong 🏓")

@bot.message_handler(commands=['report'])
def report(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Придумай абсурдну ідею для TikTok з песиками-кухарями"}],
            timeout=10  # OpenAI timeout
        )
        bot.send_message(message.chat.id, response.choices[0].message.content)
    except Exception as e:
        logging.error(f"GPT error: {e}")
        bot.send_message(message.chat.id, "GPT помилка 😢")

# Default GPT chat
@bot.message_handler(func=lambda m: True)
def gpt_chat(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message.text}],
            timeout=10
        )
        bot.send_message(message.chat.id, response.choices[0].message.content)
    except Exception as e:
        logging.error(f"GPT error: {e}")
        bot.send_message(message.chat.id, "Помилка GPT 😓")

# App entry for Gunicorn
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
