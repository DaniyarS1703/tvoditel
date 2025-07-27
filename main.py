import os
from flask import Flask, send_from_directory, request
from flask_cors import CORS
import telebot

# Настройки
TELEGRAM_TOKEN = "7943726818:AAFwDFEewyqOtVQGjzb5Uavzd7XhG1KCJcA"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

app = Flask(__name__)
CORS(app)

# 📄 Отдаём index.html
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 📄 Отдаём style.css
@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')

# 🔔 Telegram-бот: старт
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в мини-приложение 'Трезвый водитель'!")

# Запуск Flask и Telegram бота
if __name__ == '__main__':
    import threading

    def run_bot():
        bot.polling(none_stop=True)

    threading.Thread(target=run_bot).start()

    app.run(debug=True, port=5000)
