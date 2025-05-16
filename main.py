import telebot
import flask
import os

API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    json_str = flask.request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/', methods=['GET'])
def test():
    return 'Woofer Bot працює!', 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привіт! Я Woofer Bot — твій веселий SMM-помічник!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
