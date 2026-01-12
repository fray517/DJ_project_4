import telebot
from telebot.types import Message
import requests

API_URL = "http://127.0.0.1:8000/api"

BOT_TOKEN = "8392769572:AAGqC-9jJ6cPSb6eM5Inw9vPTpWeDRb7-A4"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    data = {
        "user_id": message.from_user.id,
        "username": message.from_user.username
    }
    try:
        response = requests.post(API_URL + "/register/", json=data, timeout=5)
        if response.status_code in (200, 201):
            response_data = response.json()
            if response_data.get('message'):
                bot.send_message(
                    message.chat.id,
                    "Вы уже были зарегистрированы ранее!"
                )
            else:
                bot.send_message(
                    message.chat.id,
                    f"Вы успешно зарегистрированы! "
                    f"Ваш уникальный номер: {response_data['id']}"
                )
        else:
            bot.send_message(
                message.chat.id,
                f"Произошла ошибка при регистрации! "
                f"Код ошибки: {response.status_code}"
            )
            print(f"Ошибка: {response.status_code}")
            print(f"Ответ: {response.text}")
    except requests.exceptions.ConnectionError:
        bot.send_message(
            message.chat.id,
            "Сервер временно недоступен. "
            "Пожалуйста, попробуйте позже."
        )
        print("Ошибка подключения: Django сервер не запущен")
    except requests.exceptions.Timeout:
        bot.send_message(
            message.chat.id,
            "Превышено время ожидания ответа от сервера."
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            "Произошла непредвиденная ошибка."
        )
        print(f"Неожиданная ошибка: {e}")
        
if __name__== "__main__":
    bot.polling(none_stop=True)