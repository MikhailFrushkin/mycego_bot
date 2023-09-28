from pathlib import Path

from environs import Env

path = Path(__file__).resolve().parent.parent

env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
ADMINS = env.list('ADMINS')
domain = 'https://mycego.ru'
