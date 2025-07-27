import os
import json
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Настройки
TELEGRAM_TOKEN = "7943726818:AAFwDFEewyqOtVQGjzb5Uavzd7XhG1KCJcA"
WEBHOOK_SECRET = "tvoditel-secret"
APP_URL        = "https://tvoditel.onrender.com"
ORDERS_FILE    = 'orders.json'

# Инициализация
bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)
CORS(app)

# WebApp‑страницы
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

@app.route('/client')
def client_page():
    return send_from_directory('.', 'client.html')

@app.route('/driver')
def driver_page():
    return send_from_directory('.', 'driver.html')

@app.route('/admin')
def admin_page():
    return send_from_directory('.', 'admin.html')

# Обработка формы заказа и сохранение
@app.route('/submit', methods=['POST'])
def submit_order():
    frm = request.form.get('route_from')
    to  = request.form.get('route_to')
    order = {
        'name':       request.form.get('name'),
        'phone':      request.form.get('phone'),
        'car_model':  request.form.get('car_model'),
        'route':      f"{frm} → {to}",
        'price':      request.form.get('price'),
        'city':       request.form.get('city')
    }
    orders = []
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            try:
                orders = json.load(f)
            except:
                orders = []
    orders.append(order)
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)
    print("Новая заявка:", order)
    return "Спасибо, заявка принята!"

# API для списка заявок
@app.route('/api/orders')
def api_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify([])

# API для удаления заявки по индексу
@app.route('/api/orders/<int:idx>', methods=['DELETE'])
def delete_order(idx):
    orders = []
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            orders = json.load(f)
    if 0 <= idx < len(orders):
        orders.pop(idx)
        with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)
        return '', 200
    return 'Not Found', 404

# Telegram Webhook
@app.route(f'/{WEBHOOK_SECRET}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
        bot.process_new_updates([update])
        return '', 200
    return 'Unsupported Media Type', 415

# Обработчик /start
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

# Запуск
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
