import ast
import json
import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

import bot
from data.config import path
from data.db import User
from data.api import check_user_api, create_or_get_apport, get_appointments, delete_appointments, get_works, post_works
from handlers.users.back import back
from keyboards.default.menu import menu, ready_button
from keyboards.inline.action import generate_next_week_dates_keyboard, generate_time_keyboard, generate_time_keyboard2, \
    generate_works, generate_current_week_works_dates
from loader import dp, bot
from state.states import AuthState, WorkGraf, WorkList


@dp.message_handler(commands=['start'], state='*')
async def bot_start(message: types.Message, state: FSMContext):
    """
    Старт бота, проверка на присутствие в базе данных, если нет, запрашивает пароль
    """
    logger.info('Пользователь {}: {} {} нажал на кнопку {}'.format(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username,
        message.text
    ))
    hello = ['limur.tgs', 'Dicaprio.tgs', 'hello.tgs', 'hello2.tgs', 'hello3.tgs']
    sticker = open('{}/stikers/{}'.format(path, random.choice(hello)), 'rb')
    await bot.send_sticker(message.chat.id, sticker)

    try:
        user = User.get(telegram_id=str(message.from_user.id))
        await message.answer('Добро пожаловать, {}!'
                             .format(message.from_user.first_name),
                             reply_markup=menu)
    except:
        await message.answer("Добро пожаловать, {}! Введите ваш логин:".format(message.from_user.first_name))
        await AuthState.waiting_for_login.set()


@dp.message_handler(state=AuthState.waiting_for_login)
async def process_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text

    await message.answer("Теперь введите пароль:")
    await AuthState.waiting_for_password.set()


@dp.message_handler(state=AuthState.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        login = data['login']
        password = message.text

        user_id = check_user_api(login, password)
        if user_id:
            user = User.create(telegram_id=str(message.from_user.id),
                               site_user_id=str(user_id['id']),
                               username=str(login),
                               username_tg=str(message.from_user.username),
                               first_name=str(message.from_user.first_name),
                               last_name=str(message.from_user.last_name),
                               role=str(user_id['role']),
                               )
            user.save()
            await message.answer("Доступ разрешен!", reply_markup=menu)
            await state.finish()
        else:
            await message.answer("Неверный логин или пароль. Попробуйте еще раз.")
            await message.answer("Введите ваш логин:")
            await AuthState.waiting_for_login.set()


@dp.message_handler(lambda message: not message.text.isdigit(), state=WorkList.input_num)
async def process_amount_invalid(message: types.Message):
    await message.answer("Введите число, пожалуйста.")


@dp.message_handler(state=WorkList.input_num)
async def nums_works(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        current_work = data.get('current_work')
        if current_work is None:
            await message.answer("Ошибка: вид работы не указан. Пожалуйста, выберите вид работы сначала.")
            return

        try:
            quantity = int(message.text)
            if quantity < 0:
                await message.answer("Ошибка: количество не может быть отрицательным.")
            else:
                if 'works' not in data:
                    data['works'] = {}  # Создаем словарь для хранения видов работ и их количества

                data['works'][current_work] = quantity  # Сохраняем количество работы в словарь
                await message.answer(f"Вы указали {quantity} единиц работы.")

                # После сохранения количества работы можно вернуться к выбору видов работ
                await message.answer("Выберите следующий вид работы или нажмите 'Отправить', если все работы указаны.",
                                     reply_markup=generate_works(get_works().get('data')))
                await WorkList.choice_work.set()

        except ValueError:
            await message.answer("Ошибка: введите число, пожалуйста.")


@dp.message_handler(content_types=['text'], state='*')
async def bot_message(message: types.Message, state: FSMContext):
    try:
        user = User.get(telegram_id=str(message.from_user.id))

        text = message.text
        user_id = message.from_user.id
        if text == 'Назад':
            await back(message, state)
        elif text == 'Записаться':
            await WorkGraf.choice_date.set()
            await bot.send_message(user_id, 'Выберите дату для записи:',
                                   reply_markup=generate_next_week_dates_keyboard())
        elif text == 'Мои записи':
            user_id_site = user.site_user_id

            ap_list = get_appointments(user_id_site).get('message')
            await bot.send_message(user_id, 'Записи на текущую и следующую неделю:')
            await WorkGraf.delete_row.set()
            for index, item in enumerate(ap_list, start=1):
                verified = 'Утверждено' if item[3] else 'Не утверждено'
                # Формируем текст сообщения
                message_text = f'{index}. {item[0]} с {item[1].replace(":00:00", ":00")} ' \
                               f'по {item[2].replace(":00:00", ":00")} ({verified})'

                keyboard = types.InlineKeyboardMarkup()
                delete_button = types.InlineKeyboardButton("Удалить", callback_data=f"delete_{item[4]}")
                keyboard.add(delete_button)
                if item[3]:
                    await bot.send_message(user_id, message_text)
                else:
                    await bot.send_message(user_id, message_text, reply_markup=keyboard)
        elif text == 'Заполнить лист':
            await bot.send_message(user_id, 'Выберите дату:', reply_markup=generate_current_week_works_dates())
            await WorkList.choice_date.set()

        else:
            await bot.send_message(user_id, text)

    except:
        await message.answer("Добро пожаловать! Введите ваш логин:")
        await AuthState.waiting_for_login.set()


@dp.callback_query_handler(state=[WorkGraf.choice_date])
async def process_date(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        date = callback_query.data.split('_')[1]
        data['date'] = date
        await bot.send_message(callback_query.from_user.id, 'Выберите время с:', reply_markup=generate_time_keyboard())
        await WorkGraf.choice_time.set()


@dp.callback_query_handler(state=[WorkGraf.choice_time])
async def process_time(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        start_time = callback_query.data
        data['start_time'] = start_time
        await bot.send_message(callback_query.from_user.id, 'Выберите время до:',
                               reply_markup=generate_time_keyboard2())
        await WorkGraf.choice_time2.set()


@dp.callback_query_handler(state=[WorkGraf.choice_time2])
async def process_time2(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        end_time = callback_query.data
        data['end_time'] = end_time
        user_id_site = User.get(User.telegram_id == callback_query.from_user.id).site_user_id
        print(user_id_site)
        code = create_or_get_apport(date=data['date'], start_time=data['start_time'],
                                    end_time=data['end_time'], user_id_site=user_id_site)
        if code == 200:
            await bot.send_message(callback_query.from_user.id, f'Запись на этот день уже есть')
        elif code == 401:
            await bot.send_message(callback_query.from_user.id, f'Запись создана')
        elif code == 500:
            await bot.send_message(callback_query.from_user.id, f'Ошибка')
        await state.finish()


@dp.callback_query_handler(state=[WorkGraf.delete_row])
async def del_row(callback_query: types.CallbackQuery, state: FSMContext):
    row_id = callback_query.data.split('_')[1]
    user_id_site = User.get(User.telegram_id == callback_query.from_user.id).site_user_id
    code = delete_appointments(user_id_site, row_id)
    if code == 200:
        await bot.send_message(callback_query.from_user.id, 'Запись удалена!')
    else:
        await bot.send_message(callback_query.from_user.id, 'Произошла ошибка!')
    await state.finish()


@dp.callback_query_handler(state=[WorkList.choice_date])
async def add_work(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = callback_query.data.split('_')[1]
        work_list = get_works().get('data')

        await bot.send_message(callback_query.from_user.id, 'Выберите работу:',
                               reply_markup=generate_works(work_list))
        await WorkList.choice_work.set()


@dp.callback_query_handler(state=[WorkList.choice_work, WorkList.input_num])
async def add_work(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback_query.data == 'send':
            date = data.get('date')
            works = data.get('works')
            user_id_site = User.get(User.telegram_id == callback_query.from_user.id).site_user_id
            if post_works(date, user_id_site, works) == 200:
                await bot.send_message(callback_query.from_user.id, 'Отправленно', reply_markup=menu)
            else:
                await bot.send_message(callback_query.from_user.id, 'Возникла ошибка')
        else:
            work_id = callback_query.data.split('_')
            data['current_work'] = int(work_id[1])
            await bot.send_message(callback_query.from_user.id,
                                   f'Вы ввели вид работы: {work_id[0]}.\nТеперь введите количество:')
            await WorkList.input_num.set()
