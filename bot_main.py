import os
import telebot
from telebot.types import Message
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://127.0.0.1:8000/api"
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения. "
                     "Проверьте файл .env")

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


@bot.message_handler(commands=['myinfo'])
def myinfo_command(message):
    """Получение информации о пользователе через API."""
    user_id = message.from_user.id
    try:
        response = requests.get(
            f"{API_URL}/user/{user_id}/",
            timeout=5
        )
        if response.status_code == 200:
            user_data = response.json()
            info_message = (
                f"📋 Ваша информация:\n\n"
                f"🆔 ID в базе: {user_data['id']}\n"
                f"👤 Telegram ID: {user_data['user_id']}\n"
                f"📛 Username: {user_data.get('username', 'не указан')}\n"
                f"📅 Дата регистрации: {user_data['created_at']}"
            )
            bot.send_message(message.chat.id, info_message)
        elif response.status_code == 404:
            bot.send_message(
                message.chat.id,
                "❌ Вы не зарегистрированы в системе.\n"
                "Используйте команду /start для регистрации."
            )
        else:
            bot.send_message(
                message.chat.id,
                f"⚠️ Произошла ошибка при получении информации.\n"
                f"Код ошибки: {response.status_code}"
            )
            print(f"Ошибка: {response.status_code}")
            print(f"Ответ: {response.text}")
    except requests.exceptions.ConnectionError:
        bot.send_message(
            message.chat.id,
            "🔌 Сервер временно недоступен.\n"
            "Пожалуйста, попробуйте позже."
        )
        print("Ошибка подключения: Django сервер не запущен")
    except requests.exceptions.Timeout:
        bot.send_message(
            message.chat.id,
            "⏱ Превышено время ожидания ответа от сервера."
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            "❌ Произошла непредвиденная ошибка."
        )
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    bot.polling(none_stop=True)