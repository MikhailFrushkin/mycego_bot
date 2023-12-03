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
        return self.text

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
             .order_by(fn.COUNT(Message.id).desc()).limit(10))

    # Получить минимальную дату
    min_date = Message.select(fn.date_trunc('day', fn.Min(Message.timestamp))).scalar()

    # Получить максимальную дату
    max_date = Message.select(fn.date_trunc('day', fn.Max(Message.timestamp))).scalar()

    # Преобразовать строки в объекты DateTime
    min_date = datetime.strptime(min_date, '%Y-%m-%d %H:%M:%S')
    max_date = datetime.strptime(max_date, '%Y-%m-%d %H:%M:%S')

    # Форматирование даты в строку
    min_date_str = min_date.strftime('%Y-%m-%d')
    max_date_str = max_date.strftime('%Y-%m-%d')
    return query.execute(), min_date_str, max_date_str


if __name__ == '__main__':
    results = get_message_counts_by_user()
    print(results[1], results[2])
    for result in results[0]:
        print(result)
