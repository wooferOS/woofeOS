import os
import telebot
from flask import Flask, request
import openai

# Ініціалізація токенів
TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("❌ TELEGRAM_API_TOKEN або OPENAI_API_KEY не встановлено!")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Команда /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Привіт! Я Woofer Bot — TikTok SMM помічник 🐶\n\n"
        "Доступні команди:\n"
        "/help /ping /report /today"
    )

# Команда /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "/start /help /ping /report /today — Просто напиши щось, і я відповім!"
    )

# Команда /ping
@bot.message_handler(commands=['ping'])
def ping_command(message):
    bot.send_message(message.chat.id, "Pong 🏓")

# Команда /today
@bot.message_handler(commands=['today'])
def today_command(message):
    bot.send_message(
        message.chat.id,
        "Сьогодні буде новий відео-рецепт для TikTok з песиками-кухарями! 🍔🐾"
    )

# Команда /report — GPT-звіт
@bot.message_handler(commands=['report'])
def report_command(message):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ти SMM-менеджер TikTok."},
                {"role": "user", "content": "Зроби короткий звіт за сьогоднішній TikTok контент з песиками-кухарями."}
            ],
            temperature=0.7
        )
        result = response.choices[0].message.content.strip()
        bot.send_message(message.chat.id, result)
    except Exception as e:
        bot.send_message(message.chat.id, f"GPT помилка 😢\n{e}")

# GPT-чат на всі інші повідомлення
@bot.message_handler(func=lambda message: True)
def gpt_response(message):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": message.text}
            ],
            temperature=0.7
        )
        result = response.choices[0].message.content.strip()
        bot.send_message(message.chat.id, result)
    except Exception as e:
        bot.send_message(message.chat.id, f"GPT помилка 😢\n{e}")

# Webhook (Render)
@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid content type', 403

# Запуск Flask (для Render)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
