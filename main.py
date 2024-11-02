import logging

import requests
from aiogram import Bot, Dispatcher, types, executor

API_TOKEN = '7909948711:AAHCkKp-WPjLWCq9pKDeJ5VR68EiXqax2gg'
API_OPEN_WEATHER = "388a7424c90199acd682f5b99c95c7a7"
# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Привет! Я бот Погоды!")


def get_weather_samara():
    city = 'Самара'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_OPEN_WEATHER}&units=metric&lang=ru'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        weather_desc = data['weather'][0]['description'].capitalize()
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        city_name = data['name']
        country = data['sys']['country']
        result = (
            f'🌤 Погода в {city_name}, {country}:\n'
            f'Температура: {temp}°C (ощущается как {feels_like}°C)\n'
            f'Описание: {weather_desc}\n'
            f'Влажность: {humidity}%\n'
            f'Скорость ветра: {wind_speed} м/с'
        )
        return result
    else:
        return '❌ Не удалось получить данные о погоде.'

@dp.message_handler(commands=['echo'])
async def echo(message: types.Message):

    await message.answer(message.text)


@dp.message_handler(commands=['weather'])
async def weather(message: types.Message):
    weather = get_weather_samara()
    await message.answer(weather)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
