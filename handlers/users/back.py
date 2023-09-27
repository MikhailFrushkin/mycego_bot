from aiogram.dispatcher import FSMContext

from keyboards.default import menu
from loader import bot


async def back(message, state: FSMContext):
    """Кнопка Назад, скидывает стейты и возвращает в главное меню"""
    await bot.send_message(message.from_user.id,
                           'Главное меню.',
                           reply_markup=menu)
    await state.reset_state()
    await state.finish()
