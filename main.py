import telebot
from telebot import types

#После регистрации нужно повторно отправить /start


bot = telebot.TeleBot('6440121870:AAGHtv7J_9M4G5EWSC7ZIZ9DmfWmkD1ehQE')

# Словарь для хранения информации о зарегистрированных пользователях
registered_users = {}

@bot.message_handler(commands=['start'])
def start(message):
    # Проверка, зарегистрирован ли уже пользователь
    if message.from_user.id not in registered_users:
        registered_users[message.from_user.id] = {'registered': False}

    # Если пользователь еще не зарегистрирован, начать процесс регистрации
    if not registered_users[message.from_user.id]['registered']:
        bot.send_message(message.chat.id, "Добро пожаловать! Для регистрации введите ваше имя:")
    else:
        # Добавление кнопки "Узнать тайну мира" после регистрации
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton("Узнать тайну мира")
        markup.add(item)
        bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!", reply_markup=markup)

@bot.message_handler(func=lambda message: not registered_users[message.from_user.id]['registered'])
def register_user(message):
    # Сохранение имени пользователя и запрос номера телефона
    registered_users[message.from_user.id]['name'] = message.text
    registered_users[message.from_user.id]['registered'] = True
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Отправить номер телефона", request_contact=True)
    markup.add(item)
    bot.send_message(message.chat.id, "Теперь отправьте свой номер телефона.", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    # Сохранение номера телефона и запрос локации
    registered_users[message.from_user.id]['phone'] = message.contact.phone_number
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Спасибо! Теперь отправьте свою локацию.", reply_markup=markup)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    # Сохранение локации и завершение регистрации
    registered_users[message.from_user.id]['location'] = (message.location.latitude, message.location.longitude)
    bot.send_message(
        message.chat.id,
        f"Регистрация завершена, {registered_users[message.from_user.id]['name']}!\n"
        f"Номер телефона: {registered_users[message.from_user.id]['phone']}\n"
        f"Локация: {message.location.latitude}, {message.location.longitude}"
    )

@bot.message_handler(func=lambda message: "Узнать тайну мира" in message.text)
def secret_message(message):
    # Отправка ответа бота на кнопку "Узнать тайну мира"
    bot.send_message(message.chat.id, "Не скажу тебе пока!")

bot.polling(none_stop=True)
