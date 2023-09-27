import datetime

from aiogram import executor
from loguru import logger

from data.config import path
from data.db import db, User, Message
from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
import handlers


async def on_startup(dp):
    """Установка стандартных команд, отправка сообщению админу и запуск бота"""
    date_logs = datetime.date.today()
    logger.add(sink=f"{path}/logs/logs_{date_logs}.log", level="DEBUG", format="{time} {level} {message}",
               rotation="5 MB")
    logger.info('Бот запускается')
    db.connect()
    db.create_tables([User, Message], safe=True)
    await set_default_commands(dp)
    await on_startup_notify(dp)


async def on_shutdown(dp):
    """Остановка бота"""

    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
