from aiogram import types


async def set_default_commands(dp):
    """команды бота в меню"""
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустить бота'),
        ]
    )
