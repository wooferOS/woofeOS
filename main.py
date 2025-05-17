import os
import telebot
from flask import Flask, request
import openai
import traceback
import requests
import time
from openai import OpenAI

# Ініціалізація токенів
TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("❌ TELEGRAM_API_TOKEN або OPENAI_API_KEY не встановлено!")

client = openai.OpenAI(api_key=OPENAI_API_KEY)
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
    bot.send_message(
        message.chat.id,
        "Привіт! Я Woofer Bot — TikTok SMM помічник 🐶\n\nДоступні команди:\n/help /ping /report /today"
    )

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
        print("GPT помилка:", e)
        bot.send_message(message.chat.id, "GPT помилка 😢")

# GPT-чат на всі інші повідомлення
@bot.message_handler(commands=['report'])
def report_command(message):
    try:
        thread = client.beta.threads.create()
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="Зроби короткий TikTok-звіт у стилі песика"
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id="asst_SUNoeRmHMlwxXwIRNZYAjo43"
        )

        # Очікуємо завершення відповіді
        while True:
            status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if status.status == "completed":
                break
            elif status.status == "failed":
                raise Exception("Асистент не зміг завершити відповідь.")
            time.sleep(1)

        # Отримуємо останнє повідомлення
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        reply = messages.data[0].content[0].text.value
        bot.send_message(message.chat.id, reply)

    except Exception as e:
        print("❌ GPT помилка:", e)
        traceback.print_exc()
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
