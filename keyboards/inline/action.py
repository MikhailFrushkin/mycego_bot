from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime

from loguru import logger

from data.api import get_works, get_delivery
from data.db import Works


def generate_next_week_dates_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    today = datetime.date.today()

    # Вычисляем дату начала следующей недели
    next_week_start = today - datetime.timedelta(days=7)

    for i in range(14):
        date = next_week_start + datetime.timedelta(days=i)
        button = InlineKeyboardButton(
            text=date.strftime("%Y-%m-%d"),
            callback_data=f"date_{date.strftime('%Y-%m-%d')}"
        )
        keyboard.insert(button)

    button = InlineKeyboardButton(
        text='Назад',
        callback_data='exit'
    )
    keyboard.insert(button)
    return keyboard


# Функция для создания инлайн клавиатуры с числами от 9 до 20
def generate_time_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=6)

    for num in range(9, 21):
        button = InlineKeyboardButton(
            text=str(num),
            callback_data=f"{num}:00"
        )
        keyboard.insert(button)

    return keyboard


def generate_time_keyboard2():
    keyboard = InlineKeyboardMarkup(row_width=6)

    for num in range(10, 22):
        button = InlineKeyboardButton(
            text=str(num),
            callback_data=f"{num}:00"
        )
        keyboard.insert(button)

    return keyboard


def generate_works_base():
    data = get_works().get('data')
    if data:
        Works.delete().execute()
        logger.success(data)
        for i in data:
            new_work = Works.create(id=i[0], name=i[1], delivery=i[2])


def generate_works(delivery=None):
    if delivery:
        all_works = Works.filter(delivery=True)
    else:
        all_works = Works.select()

    keyboard = InlineKeyboardMarkup(row_width=2)
    for i in all_works:
        try:
            button = InlineKeyboardButton(
                text=str(i.name),
                callback_data=f"{i.id}_{i.id}"
            )
            keyboard.insert(button)
        except:
            logger.error(i)
    button = InlineKeyboardButton(
        text='📬Отправить',
        callback_data="send"
    )
    keyboard.insert(button)

    return keyboard


def generate_current_week_works_dates():
    keyboard = InlineKeyboardMarkup(row_width=1)
    today = datetime.date.today()
    start = today - datetime.timedelta(days=6)
    for i in range(7):
        date = start + datetime.timedelta(days=i)
        if date <= today:
            button = InlineKeyboardButton(
                text=date.strftime("%Y-%m-%d"),
                callback_data=f"date_{date.strftime('%Y-%m-%d')}"
            )
            keyboard.insert(button)

    button = InlineKeyboardButton(
        text='Назад',
        callback_data='exit'
    )
    keyboard.insert(button)
    return keyboard


def create_works_list(lists):
    keyboard = InlineKeyboardMarkup(row_width=1)

    for i in lists:
        button = InlineKeyboardButton(
            text=str(i[1]),
            callback_data=f"{i[0]}_{i[1]}_{i[2]}"
        )
        keyboard.insert(button)
    button = InlineKeyboardButton(
        text='Назад',
        callback_data='exit'
    )
    keyboard.insert(button)
    return keyboard


def delete_button(data):
    keyboard = InlineKeyboardMarkup(row_width=2)
    button = InlineKeyboardButton(
        text='Удалить',
        callback_data=f'del_{data}'
    )
    keyboard.insert(button)

    button = InlineKeyboardButton(
        text='Назад',
        callback_data='exit'
    )
    keyboard.insert(button)
    return keyboard


def delivery_keyboard():
    data = get_delivery()
    keyboard = InlineKeyboardMarkup(row_width=2)
    for i in data:
        button = InlineKeyboardButton(
            text=str(i[1]),
            callback_data=f"{i[0]}"
        )
        keyboard.insert(button)
    button = InlineKeyboardButton(
        text='Назад',
        callback_data='exit'
    )
    keyboard.insert(button)
    return keyboard


call_back = InlineKeyboardMarkup(row_width=2)
button = InlineKeyboardButton(
    text='Выйти',
    callback_data='exit'
)
call_back.insert(button)
