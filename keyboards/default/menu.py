from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(row_width=2)
menu.insert(KeyboardButton('🗓Заявка в график'))
menu.insert(KeyboardButton('📕Мои записи'))
menu.insert(KeyboardButton('🔨Заполнить лист работ'))
menu.insert(KeyboardButton('📝Мои листы работ'))

second_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('Назад')],
], resize_keyboard=True)


ready_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton('Отправить')],
], resize_keyboard=True)
