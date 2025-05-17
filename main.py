import os
import telebot
from flask import Flask, request
import openai

# Ініціалізація ключів
BOT_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
openai.api_key = OPENAI_API_KEY

# Webhook endpoint
@app.route('/', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        json_str = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return 'ok', 200
    return 'Woofer Webhook OK', 200

# /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Привіт! Я Woofer Bot 🤖 Допоможу з TikTok, GPT і креативом для SMM!")

# /help
@bot.message_handler(commands=['help'])
def help_handler(message):
    commands = "/start — привітання\n/help — список команд\n/ping — перевірка\n/report — ідея від GPT\n(Напиши щось і я відповім)"
    bot.send_message(message.chat.id, commands)

# /ping
@bot.message_handler(commands=['ping'])
def ping_handler(message):
    bot.send_message(message.chat.id, "pong 🏓")

# /report — випадковий GPT-пост
@bot.message_handler(commands=['report'])
def report_handler(message):
    try:
        reply = get_gpt_response("Придумай щось цікаве або абсурдне для SMM TikTok про собак-кухарів")
        bot.send_message(message.chat.id, reply)
    except Exception:
        bot.send_message(message.chat.id, "❌ Виникла помилка при зверненні до GPT")

# GPT-відповіді на текст
@bot.message_handler(func=lambda message: True)
def gpt_response(message):
    try:
        reply = get_gpt_response(message.text)
        bot.send_message(message.chat.id, reply)
    except Exception:
        bot.send_message(message.chat.id, "😢 Не вдалося отримати відповідь від GPT.")

# GPT-логіка
def get_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        timeout=10  # безпечний таймаут
    )
    return response.choices[0].message.content.strip()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
