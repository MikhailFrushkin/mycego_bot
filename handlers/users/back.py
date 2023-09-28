from aiogram.dispatcher import FSMContext

from keyboards.default.menu import menu_keyboards
from loader import bot


async def back(message, state: FSMContext):
    """Кнопка Назад, скидывает стейты и возвращает в главное меню"""
    await bot.send_message(message.from_user.id,
                           'Главное меню.',
                           reply_markup=menu_keyboards(message.from_user.id))
    await state.reset_state()
    await state.finish()
