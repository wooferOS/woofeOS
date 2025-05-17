import os
import telebot
from flask import Flask, request
import openai
import traceback
import requests

# ENV перемінні
TOKEN = os.environ.get("TELEGRAM_API_TOKEN")
openai.api_key = os.environ.get("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# Установити webhook автоматично
def set_webhook():
    webhook_url = "https://woofer-bot.onrender.com/"
    res = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/setWebhook",
        json={"url": webhook_url}
    )
    print(f"🔗 Webhook set: {res.status_code} - {res.text}")

set_webhook()

# ================= Команди ===================
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привіт! Я Woofer Bot — TikTok SMM помічник 🐶")

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "/start /help /ping /report /today — Просто напиши щось, і я відповім!")

@bot.message_handler(commands=['ping'])
def ping_message(message):
    bot.send_message(message.chat.id, "Pong 🏓")

@bot.message_handler(commands=['today'])
def today_message(message):
    bot.send_message(message.chat.id, "Сьогодні буде новий відео-рецепт для TikTok з песиками-кухарями! 🍔🐾")

@bot.message_handler(commands=['report'])
def report_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Сформуй короткий звіт TikTok активності сьогодні."},
                {"role": "user", "content": "Зроби звіт за сьогодні"},
            ]
        )
        reply = response.choices[0].message['content']
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        print("❌ GPT помилка:", e)
        print(traceback.format_exc())
        bot.send_message(message.chat.id, "GPT помилка 😢")

# Відповідь на будь-який інший текст
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_message(message.chat.id, "Я тебе почув! 🐾")

# ================= Flask webhook ===================
@app.route('/', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/', methods=['GET'])
def index():
    return "🐾 Woofer SMM бот працює!"

# ================= Run local ===================
if __name__ == "__main__":
    print("🚀 Woofer Bot запущено. Очікуємо запити Telegram...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

