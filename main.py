import os
import telebot
from flask import Flask, request
import openai
import traceback
import requests

# Ініціалізація токенів
TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("❌ TELEGRAM_API_TOKEN або OPENAI_API_KEY не встановлено!")

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)
app = Flask(__name__)

# Встановлення webhook автоматично при старті
def set_webhook():
    webhook_url = "https://woofer-bot.onrender.com/"
    res = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook",
        json={"url": webhook_url}
    )
    print(f"🔗 Webhook status: {res.status_code} — {res.text}")

set_webhook()

# 📦 Команди
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Привіт! Я Woofer Bot — TikTok SMM помічник 🐶\n\nДоступні команди:\n/help /ping /report /today")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "/start /help /ping /report /today — Просто напиши щось, і я відповім!")

@bot.message_handler(commands=['ping'])
def ping_command(message):
    bot.send_message(message.chat.id, "Pong 🏓")

@bot.message_handler(commands=['today'])
def today_command(message):
    bot.send_message(message.chat.id, "Сьогодні буде новий відео-рецепт для TikTok з песиками-кухарями! 🍔🐾")

@bot.message_handler(commands=['report'])
def report_command(message):
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

# GPT-чат на всі інші повідомлення
@bot.message_handler(func=lambda message: True)
def gpt_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message.text}],
            temperature=0.7
        )
        result = response.choices[0].message['content'].strip()
        bot.send_message(message.chat.id, result)
    except Exception as e:
        print("GPT помилка:", e)
        print(traceback.format_exc())
        bot.send_message(message.chat.id, "GPT помилка 😢")

# Webhook POST
@app.route('/', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

# Render Healthcheck
@app.route('/', methods=['GET'])
def index():
    return "🐾 Woofer SMM бот працює!"

# Локальний запуск
if __name__ == "__main__":
    print("🚀 Woofer Bot запущено. Очікуємо запити Telegram...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
