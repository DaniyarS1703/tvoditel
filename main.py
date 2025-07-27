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
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Страницы
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

# … остальные routes без изменений …

# Главное изменение: /start передаёт user_id
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

# Webhook
@app.route(f'/{WEBHOOK_SECRET}', methods=['POST'])
def webhook():
    if request.headers.get('content-type')=='application/json':
        update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
        bot.process_new_updates([update])
        return '',200
    return 'Unsupported Media Type',415

if __name__=='__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port)
