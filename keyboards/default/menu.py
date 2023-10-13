from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.config import ADMINS


def menu_keyboards(user_id):
    menu = ReplyKeyboardMarkup(row_width=2)
    menu.insert(KeyboardButton('🗓Заявка в график'))
    menu.insert(KeyboardButton('📕Мои записи'))
    menu.insert(KeyboardButton('🔨Заполнить лист работ на день'))
    menu.insert(KeyboardButton('📝Мои листы работ за день'))
    menu.insert(KeyboardButton('🛠️Заполнить работы по поставке'))
    menu.insert(KeyboardButton('📦Мои поставки'))
    if str(user_id) in ADMINS:
        menu.insert(KeyboardButton('Обновить список работ'))
    return menu


second_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('Назад')],
], resize_keyboard=True)
