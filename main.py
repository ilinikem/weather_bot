import logging
from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

BOT_TOKEN = '6968145260:AAEoUYcNlzmdx54r6-ZG41P3O_fY1UrDJ-k'
API_ENDPOINT = 'http://127.0.0.1:8000/api/weather/'  # Замените на свой URL API


async def start(update: Update, context: CallbackContext) -> None:

    if update.message.text.lower() == 'узнать погоду':
        await update.message.reply_text('Можете ввести название города')
        return

    user = update.effective_user
    keyboard = [[{"text": "Узнать погоду", "request_location": False}]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Нажми на кнопку 'Узнать погоду'",
        reply_markup=reply_markup,
    )


async def get_weather(update: Update, context: CallbackContext) -> None:
    city_name = update.message.text
    try:
        response = requests.get(f'{API_ENDPOINT}?city={city_name}')
        response.raise_for_status()
        weather_city_name = response.json().get('city_name')
        temperature = response.json().get('temperature')
        pressure = response.json().get('pressure')
        wind_speed = response.json().get('wind_speed')
        await update.message.reply_text(
            f'Информация о погоде для города {weather_city_name}:\nТемпература: {temperature} гр.'
            f'\nДавление: {pressure} мм рт. ст.\nСкорость ветра: {wind_speed} м/с'
        )
    except requests.exceptions.RequestException as e:

        await update.message.reply_text(f'Ошибка при запросе к API:'
                                        f' Повторите запрос или попробуйте позже')


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, get_weather))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
