import os
from flask import Flask, send_from_directory
from flask_cors import CORS
import telebot
import threading

# Токен бота (можно переделать на переменные окружения позже)
TELEGRAM_TOKEN = "7943726818:AAFwDFEewyqOtVQGjzb5Uavzd7XhG1KCJcA"

# Инициализация Flask
app = Flask(__name__)
CORS(app)

# Главная страница
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Статический файл (CSS)
@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Простой хендлер
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Это мини-приложение 'Трезвый водитель' 🚘")

# Запуск бота в отдельном потоке, безопасно
def run_bot():
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout = 5)
    except Exception as e:
        print(f"[ОШИБКА БОТА] {e}")

# Стартуем бот в фоне
threading.Thread(target=run_bot).start()

# Запуск Flask-приложения
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
