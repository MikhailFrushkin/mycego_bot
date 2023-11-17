from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.config import ADMINS


def menu_keyboards(user_id=None):
    menu = ReplyKeyboardMarkup(row_width=2)
    menu.insert(KeyboardButton('🗓Заявка в график'))
    menu.insert(KeyboardButton('📕Мои записи'))
    menu.insert(KeyboardButton('🔨Заполнить лист работ на день'))
    menu.insert(KeyboardButton('📝Мои листы работ за день'))
    menu.insert(KeyboardButton('🛠️Заполнить работы по поставке'))
    menu.insert(KeyboardButton('📦Мои поставки'))
    menu.insert(KeyboardButton('😵‍💫Нормативы'))
    menu.insert(KeyboardButton('📊Статистика'))
    menu.insert(KeyboardButton('🐧Заявка на изменение'))
    if user_id and str(user_id) in ADMINS:
        menu.insert(KeyboardButton('Обновить список работ'))
        menu.insert(KeyboardButton('Статистика запросов'))
    return menu


second_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('Назад')],
], resize_keyboard=True)


type_request = ReplyKeyboardMarkup(row_width=2)
type_request.insert(KeyboardButton('График'))
type_request.insert(KeyboardButton('Лист работ'))
type_request.insert(KeyboardButton('Отпуск'))
type_request.insert(KeyboardButton('Назад'))

ready = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('Отправить')],
], resize_keyboard=True)
