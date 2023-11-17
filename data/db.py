from _datetime import datetime
from peewee import fn

from peewee import Model, CharField, ForeignKeyField, BooleanField, IntegerField, DateTimeField
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
    timestamp = DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.user.username} {self.text}'

    class Meta:
        database = db


class Works(Model):
    id = CharField(unique=True)
    name = CharField()
    delivery = BooleanField(default=False)
    standard = IntegerField(default=0)

    class Meta:
        database = db


def get_message_counts_by_user():
    # Запрос, который группирует записи по полю text и считает количество записей в каждой группе
    query = (Message
             .select(Message.text, fn.COUNT(Message.id).alias('count'))
             .group_by(Message.text)
             .order_by(fn.COUNT(Message.id).desc()))

    # Выполнение запроса и получение результатов
    results = query.execute()
    return results

    # query = (Message
    #          .select(User.username, Message.text, fn.COUNT(Message.id).alias('count'))
    #          .join(User)
    #          .group_by(User.username, Message.text))
    #
    # # Выполнение запроса и получение результатов
    # results = query.execute()
    #
    # # Вывод уникальных значений и их количества для каждого пользователя
    # for result in results:
    #     print(f'Пользователь: {result.user.username}, Text: {result.text}, Количество: {result.count}')


if __name__ == '__main__':
    # Вызовем функцию для получения данных
    get_message_counts_by_user()
