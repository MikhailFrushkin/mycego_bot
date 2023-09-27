from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime


def generate_next_week_dates_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    today = datetime.date.today()

    # Найдем день недели для текущей даты (0 - понедельник, 6 - воскресенье)
    current_weekday = today.weekday()

    # Вычисляем разницу дней для начала следующей недели (пн)
    days_until_next_monday = (7 - current_weekday) % 7

    # Вычисляем дату начала следующей недели
    next_week_start = today + datetime.timedelta(days=days_until_next_monday - 7)

    for i in range(14):
        date = next_week_start + datetime.timedelta(days=i)
        button = InlineKeyboardButton(
            text=date.strftime("%Y-%m-%d"),
            callback_data=f"date_{date.strftime('%Y-%m-%d')}"
        )
        keyboard.insert(button)

    return keyboard


# Функция для создания инлайн клавиатуры с числами от 9 до 20
def generate_time_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=4)

    for num in range(9, 21):
        button = InlineKeyboardButton(
            text=str(num),
            callback_data=f"{num}:00"
        )
        keyboard.insert(button)

    return keyboard


def generate_time_keyboard2():
    keyboard = InlineKeyboardMarkup(row_width=4)

    for num in range(10, 22):
        button = InlineKeyboardButton(
            text=str(num),
            callback_data=f"{num}:00"
        )
        keyboard.insert(button)

    return keyboard


def generate_works(works_list):
    keyboard = InlineKeyboardMarkup(row_width=2)

    for i in works_list:
        button = InlineKeyboardButton(
            text=str(i[1]),
            callback_data=f"{i[1]}_{i[0]}"
        )
        keyboard.insert(button)

    button = InlineKeyboardButton(
        text='Отправить',
        callback_data="send"
    )
    keyboard.insert(button)

    return keyboard


def generate_current_week_works_dates():
    keyboard = InlineKeyboardMarkup(row_width=2)
    today = datetime.date.today()

    # Найдем день недели для текущей даты (0 - понедельник, 6 - воскресенье)
    current_weekday = today.weekday()

    # Вычисляем разницу дней для начала следующей недели (пн)
    days_until_next_monday = (7 - current_weekday) % 7

    # Вычисляем дату начала следующей недели
    next_week_start = today + datetime.timedelta(days=days_until_next_monday - 7)

    for i in range(7):
        date = next_week_start + datetime.timedelta(days=i)
        button = InlineKeyboardButton(
            text=date.strftime("%Y-%m-%d"),
            callback_data=f"date_{date.strftime('%Y-%m-%d')}"
        )
        keyboard.insert(button)

    return keyboard