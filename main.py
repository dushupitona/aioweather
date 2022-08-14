from aiogram import Bot, Dispatcher, executor, types
from config import tokenn
import time
from datetime import datetime
import pytz
import requests
from bs4 import BeautifulSoup
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


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



set_time = ''




storage = MemoryStorage()
bot = Bot(token=tokenn)
dp = Dispatcher(bot, storage=storage)

class UserState(StatesGroup):
    name = State()
url = 'https://yandex.com.am/weather/'
response = requests.get(url)
src = response.text
soup = BeautifulSoup(src, 'lxml')


@dp.message_handler(commands="start")
async def strt(message: types.Message):
    try:
        button1 = KeyboardButton('/weather')
        button2 = KeyboardButton('/time')
        markup = ReplyKeyboardMarkup().add(button1).add(button2)
        await message.answer('Привет', reply_markup=markup)
        while True:
            a = pytz.timezone('Asia/Barnaul')
            now = datetime.now(a)
            timme = now.strftime('%H:%M:%S')
            datte = str(now.date())
            year = datte[:4]
            month = datte[5:7]
            day = datte[8:]
            #
            if timme == set_time:
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
    await UserState.name.set()

@dp.message_handler(state=UserState.name)
async def get_username(message: types.Message, state: FSMContext):
    global set_time
    await state.update_data(username=message.text)
    await message.answer('Как скажешь')
    data = await state.get_data()
    set_time = data['username']
    await state.finish()


@dp.message_handler(commands="weather")
async def show_wther(message: types.Message):
    try:
        wth = soup.find(class_='temp fact__temp fact__temp_size_s')
        h2d = soup.find(class_='link__condition day-anchor i-bem')
        rain = soup.find(class_='maps-widget-fact__title')
        await message.answer( f'Температура {wth.text}, на улице {(h2d.text).lower()}. {rain.text}.')
    except:
        await message.answer("Что-то пошло не так")
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
