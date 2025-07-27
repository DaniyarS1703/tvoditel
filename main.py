import os
import json
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from werkzeug.utils import secure_filename

# Настройки
TELEGRAM_TOKEN = "7943726818:AAFwDFEewyqOtVQGjzb5Uavzd7XhG1KCJcA"
WEBHOOK_SECRET = "tvoditel-secret"
APP_URL        = "https://tvoditel.onrender.com"
ORDERS_FILE    = 'orders.json'
DRIVERS_FILE   = 'drivers.json'
UPLOAD_FOLDER  = 'avatars'
ALLOWED_EXT    = {'png','jpg','jpeg','gif'}

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)
CORS(app)

# Папка для аватарок
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# WebApp‑страницы
@app.route('/')
def index():     return send_from_directory('.', 'index.html')
@app.route('/style.css')
def style():     return send_from_directory('.', 'style.css')
@app.route('/order')
def order():     return send_from_directory('.', 'order.html')
@app.route('/list')
def lst():       return send_from_directory('.', 'list.html')
@app.route('/client')
def client():    return send_from_directory('.', 'client.html')
@app.route('/driver')
def driver():    return send_from_directory('.', 'driver.html')
@app.route('/admin')
def admin():     return send_from_directory('.', 'admin.html')
@app.route('/avatars/<filename>')
def avatars(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Обработка формы заказа
@app.route('/submit', methods=['POST'])
def submit_order():
    # ... ваш код для заказов без изменений ...
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
            try: orders = json.load(f)
            except: orders = []
    orders.append(order)
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)
    return "Спасибо, заявка принята!"

# API для списка заказов
@app.route('/api/orders')
def api_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route('/api/orders/<int:idx>', methods=['DELETE'])
def delete_order(idx):
    # ... ваш код для удаления заказа без изменений ...
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

# === Вот что нужно добавить ===

# Регистрация водителей (POST)
@app.route('/api/drivers', methods=['POST'])
def register_driver():
    tg_id = request.form.get('tg_id')
    name  = request.form.get('name')
    city  = request.form.get('city')
    data  = {'tg_id': tg_id, 'name': name, 'city': city}

    # Сохранение аватара (если есть)
    if 'avatar' in request.files:
        f = request.files['avatar']
        ext = f.filename.rsplit('.',1)[-1].lower()
        if ext in ALLOWED_EXT:
            fn = secure_filename(f"{tg_id}.{ext}")
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))
            data['avatar'] = f"/avatars/{fn}"

    drivers = []
    if os.path.exists(DRIVERS_FILE):
        with open(DRIVERS_FILE, 'r', encoding='utf-8') as f:
            try: drivers = json.load(f)
            except: drivers = []
    drivers.append(data)
    with open(DRIVERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(drivers, f, ensure_ascii=False, indent=2)
    return jsonify({'status':'ok'})

# Получение списка водителей (GET)
@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    if os.path.exists(DRIVERS_FILE):
        with open(DRIVERS_FILE, 'r', encoding='utf-8') as f:
            try: data = json.load(f)
            except: data = []
        return jsonify(data)
    return jsonify([])

# === Конец добавления ===

# Telegram Webhook и /start (без изменений)
@app.route(f'/{WEBHOOK_SECRET}', methods=['POST'])
def webhook():
    if request.headers.get('content-type')=='application/json':
        update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
        bot.process_new_updates([update])
        return '',200
    return 'Unsupported Media Type',415

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    webapp_url = f"{APP_URL}?user_id={user_id}"
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    wb = WebAppInfo(url=webapp_url)
    kb.add(KeyboardButton("Открыть мини‑приложение", web_app=wb))
    bot.send_message(message.chat.id,
                     "Добро пожаловать! Нажмите кнопку для открытия приложения:",
                     reply_markup=kb)

if __name__=='__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port)
