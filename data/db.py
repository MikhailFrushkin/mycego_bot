from peewee import Model, CharField, ForeignKeyField, BooleanField, IntegerField
from playhouse.sqlite_ext import SqliteDatabase

# Инициализируйте базу данных SQLite
db = SqliteDatabase('telegram_bot.db')


class User(Model):
    telegram_id = CharField(unique=True)
    site_user_id = CharField(unique=True, null=True)
    username = CharField(unique=True, null=True)
    username_tg = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    role = CharField(null=True)

    class Meta:
        database = db


class Message(Model):
    user = ForeignKeyField(User, backref='messages')
    text = CharField()
    timestamp = CharField()  # Можно использовать datetime вместо строки, чтобы хранить временные метки

    class Meta:
        database = db


class Works(Model):
    id = CharField(unique=True)
    name = CharField()
    delivery = BooleanField(default=False)
    standard = IntegerField(default=0)

    class Meta:
        database = db