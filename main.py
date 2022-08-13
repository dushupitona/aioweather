from aiogram import Bot, Dispatcher, executor, types
from config import tokenn
import time
from datetime import datetime
import pytz
import requests
from bs4 import BeautifulSoup
import asyncio


def remonth(x):
    x = int(x)
    if x == 1:
        return 'января'
    if x == 2:
        return 'февраля'
    if x == 3:
        return 'марта'
    if x == 4:
        return 'апреля'
    if x == 5:
        return 'мая'
    if x == 6:
        return 'июня'
    if x == 7:
        return 'июля'
    if x == 8:
        return 'августа'
    if x == 9:
        return 'сентября'
    if x == 10:
        return 'октября'
    if x == 11:
        return 'ноября'
    if x == 12:
        return 'декабря'


bot = Bot(token=tokenn)
dp = Dispatcher(bot)


url = 'https://yandex.com.am/weather/'
response = requests.get(url)
src = response.text
soup = BeautifulSoup(src, 'lxml')


@dp.message_handler(commands="start")
async def strt(message: types.Message):
    try:
        while True:
            a = pytz.timezone('Asia/Barnaul')
            now = datetime.now(a)
            timme = now.strftime('%H:%M:%S')
            datte = str(now.date())
            year = datte[:4]
            month = datte[5:7]
            day = datte[8:]
            #
            wth = soup.find(class_='temp fact__temp fact__temp_size_s')
            h2d = soup.find(class_='link__condition day-anchor i-bem')
            rain = soup.find(class_='maps-widget-fact__title')
            await message.answer(
                             f'Доброе утро, капитан, сегодня {day} {remonth(month)}, за бортом {(h2d.text).lower()}, по градусной\
             шкале {wth.text}. {rain.text}. ', reply_markup=types.ReplyKeyboardRemove()
            )
            await asyncio.sleep(1)
    except:
        await message.answer("Что-то пошло не так")


@dp.message_handler(commands="time")
async def set_time(message:types.Message):
    await message.answer('Введи время, когда хочешь получить погоду.')


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)