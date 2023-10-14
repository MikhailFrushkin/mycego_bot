from pathlib import Path

from environs import Env

path = Path(__file__).resolve().parent.parent

env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN2')
GPT_TOKEN = env.str('GPT_TOKEN')
ADMINS = env.list('ADMINS')
domain = 'http://127.0.0.1:8000'
