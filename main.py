from flask import Flask, request
import telebot
import os

TOKEN = os.getenv("TELEGRAM_API_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

# Commands
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привіт! Я Woofer Bot — допоможу з TikTok 🌭")

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "/start /help /ping /today /report")

@bot.message_handler(commands=['ping'])
def ping_message(message):
    bot.send_message(message.chat.id, "pong 🏓")

# You can expand other handlers below...
