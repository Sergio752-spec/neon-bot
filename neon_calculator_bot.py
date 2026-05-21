import telebot
from telebot import types

TOKEN = 'ТВОЙ_ТОКЕН_БОТА'
bot = telebot.TeleBot(TOKEN)

user_data = {}

# СТАРТ
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("📦 Рассчитать вывеску")
    markup.add(btn)

    bot.send_message(
        message.chat.id,
        "Добро пожаловать в калькулятор неоновых вывесок",
        reply_markup=markup
    )

# КНОПКА РАСЧЕТА
@bot.message_handler(func=lambda message: message.text == "📦 Рассчитать вывеску")
def ask_name(message):
    bot.send_message(message.chat.id, "Введите название вывески:")
    bot.register_next_step_handler(message, get_name)

# НАЗВАНИЕ
def get_name(message):
    user_data[message.chat.id] = {}
    user_data[message.chat.id]['name'] = message.text

    bot.send_message(message.chat.id, "Введите длину неона в метрах:")
    bot.register_next_step_handler(message, get_neon)

# НЕОН
def get_neon(message):
    try:
        neon = float(message.text.replace(',', '.'))
        user_data[message.chat.id]['neon'] = neon

        bot.send_message(message.chat.id, "Введите площадь пластика (м²):")
        bot.register_next_step_handler(message, get_plastic)

    except:
        bot.send_message(message.chat.id, "Введите число!")
        bot.register_next_step_handler(message, get_neon)

# ПЛАСТИК И РАСЧЕТ
def get_plastic(message):
    try:
        plastic_area = float(message.text.replace(',', '.'))

        data = user_data[message.chat.id]

        name = data['name']
        neon = data['neon']

        # НЕОН
        neon_cost = neon * 140

        # БЛОК ПИТАНИЯ
        if neon <= 4:
            psu = 190
        elif neon <= 6:
            psu = 230
        elif neon <= 8:
            psu = 350
        elif neon <= 11:
            psu = 450
        else:
            psu = 900

        # ДИММЕР
        if neon <= 5:
            dimmer = 90
        else:
            dimmer = 290

        # ПЛАСТИК
        plastic = plastic_area * 1000

        # ФРЕЗЕРОВКА
        frezer = neon * 1.38 * 25

        # РАБОТА
        labor_hours = (neon * 25) / 60
        labor = labor_hours * 400

        if neon > 6:
            labor *= 1.5

        # ДОПОЛНИТЕЛЬНО
        delivery = 300
        pack = 150
        mount = 50

        total = (
            neon_cost +
            psu +
            dimmer +
            plastic +
            frezer +
            labor +
            delivery +
            pack +
            mount
        )

        result = f"""
📦 Название: {name}

📏 Неон: {neon} м
🧱 Пластик: {plastic_area} м²

💡 Неон: {neon_cost:.0f} грн
🔌 Блок питания: {psu} грн
🎛 Диммер: {dimmer} грн
🪚 Фрезеровка: {frezer:.0f} грн
🧱 Пластик: {plastic:.0f} грн
👨‍🔧 Работа: {labor:.0f} грн
🚚 Доставка: {delivery} грн
📦 Упаковка: {pack} грн
🔩 Крепление: {mount} грн

💰 ИТОГО: {total:.0f} грн
"""

        bot.send_message(message.chat.id, result)

    except:
        bot.send_message(message.chat.id, "Введите число!")
        bot.register_next_step_handler(message, get_plastic)

print("Бот запущен...")
bot.infinity_polling()
