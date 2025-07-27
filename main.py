import os
from flask import Flask, send_from_directory
from flask_cors import CORS
import telebot
import threading
import time

TELEGRAM_TOKEN = "7943726818:AAFwDFEewyqOtVQGjzb5Uavzd7XhG1KCJcA"

app = Flask(__name__)
CORS(app)

# Главная страница
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Стили
@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')

# Бот
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Привет! Это мини-приложение 'Трезвый водитель' 🚘")

# Защита от падения polling
def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"[Bot Error] {e}")
            time.sleep(5)

# Запуск в фоне
threading.Thread(target=run_bot).start()

# Запуск Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
