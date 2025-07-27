import os
from flask import Flask, request, send_from_directory
from flask_cors import CORS
import telebot

TELEGRAM_TOKEN = "7943726818:AAFwDFEewyqOtVQGjzb5Uavzd7XhG1KCJcA"
WEBHOOK_SECRET = "tvoditel-secret"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)
CORS(app)

# Главная страница
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')

# Обработка Webhook от Telegram
@app.route(f'/{WEBHOOK_SECRET}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Unsupported Media Type', 415

# Пример обработчика команд
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Это бот 'Трезвый водитель' 🚘")

# Запуск сервера
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
