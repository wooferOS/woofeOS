import os
import telebot
import openai
from flask import Flask, request
import threading

# Змінні середовища
BOT_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY
app = Flask(__name__)

# GPT-запит
def get_gpt_reply(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        timeout=10
    )
    return response.choices[0].message.content.strip()

# Вебхук
@app.route('/', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.data.decode("utf-8"))
        threading.Thread(target=bot.process_new_updates, args=([update],)).start()
        return 'OK', 200
    return 'Woofer Webhook OK', 200

# Команди
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привіт! Я Woofer 🤖 Спробуй /help")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "/start /help /ping /report")

@bot.message_handler(commands=['ping'])
def handle_ping(message):
    bot.send_message(message.chat.id, "pong 🏓")

@bot.message_handler(commands=['report'])
def handle_report(message):
    try:
        idea = get_gpt_reply("Придумай щось цікаве або абсурдне для TikTok про собак-кухарів")
        bot.send_message(message.chat.id, idea)
    except:
        bot.send_message(message.chat.id, "GPT щось не відповів 😔")

# GPT-чат
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        reply = get_gpt_reply(message.text)
        bot.send_message(message.chat.id, reply)
    except:
        bot.send_message(message.chat.id, "Щось пішло не так 😔")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
