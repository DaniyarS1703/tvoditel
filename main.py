import os
from flask import Flask, send_from_directory, request
from flask_cors import CORS
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

TELEGRAM_TOKEN = "7943726818:AAFwDFEewyqOtVQGjzb5Uavzd7XhG1KCJcA"
WEBHOOK_SECRET = "tvoditel-secret"
APP_URL = "https://tvoditel.onrender.com"

app = Flask(__name__)
CORS(app)

# WebApp страницы
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')

@app.route('/order')
def order_page():
    return send_from_directory('.', 'order.html')

@app.route('/list')
def list_page():
    return send_from_directory('.', 'list.html')

@app.route('/submit', methods=['POST'])
def submit_order():
    data = {k: request.form.get(k) for k in ('name','phone','car_model','route','price','city')}
    print("Новая заявка:", data)
    return "Спасибо, заявка принята!"

# Telegram Webhook
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@app.route(f'/{WEBHOOK_SECRET}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
        bot.process_new_updates([update])
        return '', 200
    return 'Unsupported Media Type', 415

# /start с WebApp‑кнопкой
@bot.message_handler(commands=['start'])
def start(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    wb = WebAppInfo(url=APP_URL)
    kb.add(KeyboardButton("Открыть мини‑приложение", web_app=wb))
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Нажмите кнопку для открытия приложения:",
        reply_markup=kb
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
