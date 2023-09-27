from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(row_width=2)
menu.insert(KeyboardButton('Записаться'))
menu.insert(KeyboardButton('Мои записи'))
menu.insert(KeyboardButton('Заполнить лист'))
menu.insert(KeyboardButton('Мои листы'))

second_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('Назад')],
], resize_keyboard=True)


ready_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('Отправить')],
], resize_keyboard=True)
