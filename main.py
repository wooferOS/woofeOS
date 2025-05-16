from flask import Flask, request
import telebot
import os
import openai

# Ініціалізація токенів
TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# GPT-клієнт
openai.api_key = OPENAI_API_KEY

@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

# /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привіт! Я Woofer Bot — допоможу з TikTok 🌭")

# /help
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "/start /help /ping /today /report\nПросто напиши щось — я відповім 🧠")

# /ping
@bot.message_handler(commands=['ping'])
def ping_message(message):
    bot.send_message(message.chat.id, "pong 🏓")

# /report — щось випадкове з GPT
@bot.message_handler(commands=['report'])
def report_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Придумай щось цікаве або абсурдне для SMM TikTok про собак-кухарів"}]
        )
        reply = response.choices[0].message.content
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, "Помилка при отриманні ідеї 😢")

# Обробка звичайних повідомлень (GPT-чат)
@bot.message_handler(func=lambda message: True)
def gpt_chat(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message.text}]
        )
        reply = response.choices[0].message.content
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, "Щось пішло не так з GPT 😢")
