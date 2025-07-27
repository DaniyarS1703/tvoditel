import os
from flask import Flask, send_from_directory, request
from flask_cors import CORS
import telebot

# 1) Настройки
TELEGRAM_TOKEN = "7943726818:AAFwDFEewyqOtVQGjzb5Uavzd7XhG1KCJcA"
WEBHOOK_SECRET = "tvoditel-secret"

# 2) Инициализация
bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)
CORS(app)

# 3) Маршруты для веба
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')

@app.route('/order')
def order_page():
    return send_from_directory('.', 'order.html')

@app.route('/submit', methods=['POST'])
def submit_order():
    data = {
        'name':       request.form.get('name'),
        'phone':      request.form.get('phone'),
        'car_model':  request.form.get('car_model'),
        'route':      request.form.get('route'),
        'price':      request.form.get('price'),
        'city':       request.form.get('city')
    }
    # Здесь вы можете сохранить data в БД или отправить менеджеру
    print("Новая заявка:", data)
    return "Спасибо, заявка принята!"

# 4) Webhook для Telegram
@app.route(f'/{WEBHOOK_SECRET}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
        bot.process_new_updates([update])
        return '', 200
    return 'Unsupported Media Type', 415

# 5) Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Это бот 'Трезвый водитель' 🚘")

# 6) Запуск Flask
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
