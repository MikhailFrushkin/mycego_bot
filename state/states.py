from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State


class AuthState(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()


class WorkGraf(StatesGroup):
    choice_date = State()
    choice_time = State()
    choice_time2 = State()
    delete_row = State()


class WorkList(StatesGroup):
    choice_date = State()
    choice_work = State()
    input_num = State()
    send_comment = State()


class WorkListDelivery(StatesGroup):
    choice_date = State()
    choice_delivery = State()
    choice_work = State()
    input_num = State()


class ViewWorkList(StatesGroup):
    view_work = State()
    del_work = State()
