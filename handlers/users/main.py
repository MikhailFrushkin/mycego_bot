import ast
import json
import os
import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

import bot
from data.config import path
from data.db import User
from data.api import check_user_api, create_or_get_apport, get_appointments, delete_appointments, get_works, post_works, \
    get_works_lists, get_details_works_lists, del_works_lists, get_data_delivery
from handlers.users.back import back
from keyboards.default.menu import menu_keyboards
from keyboards.inline.action import generate_next_week_dates_keyboard, generate_time_keyboard, generate_time_keyboard2, \
    generate_works, generate_current_week_works_dates, create_works_list, delete_button, generate_works_base, \
    delivery_keyboard, call_back
from loader import dp, bot
from state.states import AuthState, WorkGraf, WorkList, ViewWorkList, WorkListDelivery


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
    await back(message, state)

    hello = os.listdir('stickers')
    sticker = open('{}/stickers/{}'.format(path, random.choice(hello)), 'rb')
    await bot.send_sticker(message.chat.id, sticker)

    try:
        user = User.get(telegram_id=str(message.from_user.id))
        await message.answer('Добро пожаловать, {}!'
                             .format(message.from_user.first_name),
                             reply_markup=menu_keyboards(message.from_user.id))
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
            await message.answer("Доступ разрешен!", reply_markup=menu_keyboards(message.from_user.id))
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
                mes = await message.answer(
                    "Выберите следующий вид работы или нажмите 'Отправить', если все работы указаны.",
                    reply_markup=generate_works())
                data['mes'] = mes
                await WorkList.choice_work.set()

        except ValueError:
            await message.answer("Ошибка: введите число, пожалуйста.", reply_markup=call_back)


@dp.message_handler(state=WorkListDelivery.input_num)
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
                mes = await message.answer(
                    "Выберите следующий вид работы или нажмите 'Отправить', если все работы указаны.",
                    reply_markup=generate_works(delivery=True))
                data['mes'] = mes
                await WorkListDelivery.choice_work.set()

        except ValueError:
            await message.answer("Ошибка: введите число, пожалуйста.", reply_markup=call_back)


@dp.message_handler(content_types=['text'], state='*')
async def bot_message(message: types.Message, state: FSMContext):
    try:
        user = User.get(telegram_id=str(message.from_user.id))
        user_id_site = user.site_user_id
        text = message.text
        user_id = message.from_user.id
        if text == 'Назад':
            await back(message, state)
        elif text == '🗓Заявка в график':
            await WorkGraf.choice_date.set()
            await bot.send_message(user_id, 'Выберите дату для записи:',
                                   reply_markup=generate_next_week_dates_keyboard())
        elif text == '📕Мои записи':

            ap_list = get_appointments(user_id_site).get('message')
            await bot.send_message(user_id, 'Записи на текущую и следующую неделю:')
            await WorkGraf.delete_row.set()
            for index, item in enumerate(ap_list, start=1):
                verified = '✅Утверждено' if item[3] else '⛔️Не утверждено'
                message_text = f'{index}. {item[0]} с {item[1].replace(":00:00", ":00")} ' \
                               f'по {item[2].replace(":00:00", ":00")} \n{verified}'

                keyboard = types.InlineKeyboardMarkup()
                delete_button = types.InlineKeyboardButton("🚫Удалить", callback_data=f"delete_{item[4]}")
                keyboard.add(delete_button)
                if item[3]:
                    await bot.send_message(user_id, message_text)
                else:
                    await bot.send_message(user_id, message_text, reply_markup=keyboard)
        elif text == '🔨Заполнить лист работ на день':
            async with state.proxy() as data:
                mes = await bot.send_message(user_id, 'Выберите дату:',
                                             reply_markup=generate_current_week_works_dates())
                data['mes'] = mes
                await WorkList.choice_date.set()

        elif text == '📝Мои листы работ за день':
            works_lists = get_works_lists(user_id_site).get('data')
            if len(works_lists) > 0:
                async with state.proxy() as data:
                    mes = await bot.send_message(user_id, "Ваши сдельные листы:",
                                                 reply_markup=create_works_list(works_lists))
                    data['mes'] = mes
                    await ViewWorkList.view_work.set()

            else:
                await bot.send_message(user_id, "Ни чего не найдено", reply_markup=menu_keyboards(message.from_user.id))
        elif text == '🛠️Заполнить работы по поставке':
            async with state.proxy() as data:
                mes = await bot.send_message(user_id, 'Выберите дату:',
                                             reply_markup=generate_current_week_works_dates())
                data['mes'] = mes
                await WorkListDelivery.choice_date.set()
        elif text == '📦Мои поставки':
            await bot.send_message(user_id, "Ваши сдельные листы на поставки за неделю:",
                                   reply_markup=menu_keyboards(message.from_user.id))
            user_id_site = User.get(User.telegram_id == message.from_user.id).site_user_id
            data_delivery = get_data_delivery(user_id_site).get('data', None)
            if data_delivery:
                message_bot = ''
                for key, value in data_delivery.items():
                    message_bot += f"\n{key}\n"
                    for i, j in value.items():
                        message_bot += f'    {i}: {j}\n'
                await bot.send_message(user_id, message_bot)
            else:
                await bot.send_message(user_id, "Не найдено за неделю",
                                       reply_markup=menu_keyboards(message.from_user.id))
        elif text == 'Обновить список работ':
            generate_works_base()
        else:
            await bot.send_message(user_id, text)

        await bot.send_message(880277049,
                               f'{user.username} - {message.text}')
    except Exception as ex:
        logger.error(ex)
        await back(message, state)
        # await message.answer("Добро пожаловать! Введите ваш логин:")
        # await AuthState.waiting_for_login.set()


@dp.callback_query_handler(state=[WorkGraf.choice_date])
async def process_date(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback_query.data == 'exit':
            await back(callback_query, state)
        else:
            date = callback_query.data.split('_')[1]
            data['date'] = date
            await bot.send_message(callback_query.from_user.id, 'Выберите время с:',
                                   reply_markup=generate_time_keyboard())
            await WorkGraf.choice_time.set()


@dp.callback_query_handler(state=[WorkGraf.choice_time])
async def process_time(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'exit':
        await back(callback_query, state)
    else:
        async with state.proxy() as data:
            start_time = callback_query.data
            data['start_time'] = start_time
            await bot.send_message(callback_query.from_user.id, 'Выберите время до:',
                                   reply_markup=generate_time_keyboard2())
            await WorkGraf.choice_time2.set()


@dp.callback_query_handler(state=[WorkGraf.choice_time2])
async def process_time2(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'exit':
        await back(callback_query, state)
    else:
        async with state.proxy() as data:
            end_time = callback_query.data
            data['end_time'] = end_time
            if int(data['end_time'].replace(':00', '')) < int(data['start_time'].replace(':00', '')):
                await bot.send_message(callback_query.from_user.id,
                                       'Время завершение не должно быть меньше времени начала!',
                                       reply_markup=menu_keyboards(callback_query.from_user.id))
            else:
                user_id_site = User.get(User.telegram_id == callback_query.from_user.id).site_user_id
                code = create_or_get_apport(date=data['date'], start_time=data['start_time'],
                                            end_time=data['end_time'], user_id_site=user_id_site)
                if code == 401:
                    await bot.send_message(callback_query.from_user.id, f'🛑Запись на этот день уже есть🛑')
                elif code == 200:
                    await bot.send_message(callback_query.from_user.id, f'✅Запись создана✅')
                elif code == 403:
                    await bot.send_message(callback_query.from_user.id, f'❌Вы не работаете❌')
                elif code == 500:
                    await bot.send_message(callback_query.from_user.id, f'☣️Ошибка☣️')
            await state.finish()


@dp.callback_query_handler(state=[WorkGraf.delete_row])
async def del_row(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'exit':
        await back(callback_query, state)
    else:
        row_id = callback_query.data.split('_')[1]
        user_id_site = User.get(User.telegram_id == callback_query.from_user.id).site_user_id
        code = delete_appointments(user_id_site, row_id)
        if code == 200:
            await bot.send_message(callback_query.from_user.id, '✅Запись удалена!✅')
        else:
            await bot.send_message(callback_query.from_user.id, '☣️Произошла ошибка!☣️')
        await state.finish()


@dp.callback_query_handler(state=[WorkList.choice_date])
async def add_work_list(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'exit':
        await back(callback_query, state)
    else:
        async with state.proxy() as data:
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=data['mes'].message_id)
            date = callback_query.data.split('_')[1]
            data['date'] = date
            mes = await bot.send_message(callback_query.from_user.id, f'{date}\nВыберите работу:',
                                         reply_markup=generate_works())
            data['mes'] = mes
            await WorkList.choice_work.set()


@dp.callback_query_handler(state=[WorkList.choice_work, WorkList.input_num])
async def add_works(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'exit':
        await back(callback_query, state)
    else:
        async with state.proxy() as data:
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=data['mes'].message_id)
            if callback_query.data == 'send':
                date = data.get('date')
                works = data.get('works')
                if not works:
                    await bot.send_message(callback_query.from_user.id, '❗️Вы ни чего не заполнил, чтобы отправлять❗️',
                                           reply_markup=menu_keyboards(callback_query.from_user.id))
                else:
                    user_id_site = User.get(User.telegram_id == callback_query.from_user.id).site_user_id
                    code = post_works(date, user_id_site, works)
                    if code == 200:
                        mes = '✅Отправленно✅'
                    elif code == 401:
                        mes = '🛑Запись на эту дату существует🛑'
                    elif code == 403:
                        mes = '❌Вы не работаете❌'
                    else:
                        mes = '☣️Возникла ошибка☣️'
                    await bot.send_message(callback_query.from_user.id, mes,
                                           reply_markup=menu_keyboards(callback_query.from_user.id))
                await state.reset_state()
                await state.finish()
            else:
                work_id = callback_query.data.split('_')
                data['current_work'] = int(work_id[1])
                await bot.send_message(callback_query.from_user.id,
                                       f'Теперь введите количество:')
                await WorkList.input_num.set()


@dp.callback_query_handler(state=[ViewWorkList.view_work])
async def view_work(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'exit':
        await back(callback_query, state)
    else:
        async with state.proxy() as data:
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=data['mes'].message_id)

            work_id = callback_query.data.split('_')
            is_checked = work_id[2]
            data = get_details_works_lists(work_id[0]).get('data')
            if isinstance(data, dict):
                mes = f'{work_id[1]}\n'
                mes += '✅Утверждено' if is_checked == 'True' else '⛔️Не утверждено'
                for key, value in data.items():
                    mes += f'\n{key} - {value}'
                if not is_checked == 'True':
                    await bot.send_message(callback_query.from_user.id, mes, reply_markup=delete_button(work_id[0]))
                    await ViewWorkList.del_work.set()
                else:
                    await bot.send_message(callback_query.from_user.id, mes)

            else:
                await bot.send_message(callback_query.from_user.id, data)


@dp.callback_query_handler(state=[ViewWorkList.del_work])
async def del_work(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'exit':
        await back(callback_query, state)
    else:
        work_id = int(callback_query.data.split('_')[1])
        user_id_site = User.get(User.telegram_id == callback_query.from_user.id).site_user_id
        code = del_works_lists(work_id, user_id_site)
        if code == 200:
            await bot.send_message(callback_query.from_user.id, '✅Запись удалена✅',
                                   reply_markup=menu_keyboards(callback_query.from_user.id))
        else:
            await bot.send_message(callback_query.from_user.id, '⛔️Произошла ошибка удаления⛔️',
                                   reply_markup=menu_keyboards(callback_query.from_user.id))


@dp.callback_query_handler(state=[WorkListDelivery.choice_date])
async def add_delivery_date(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'exit':
        await back(callback_query, state)
    else:
        async with state.proxy() as data:
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=data['mes'].message_id)
            date = callback_query.data.split('_')[1]
            data['date'] = date
            mes = await bot.send_message(callback_query.from_user.id, f'{date}\nВыберите поставку:',
                                         reply_markup=delivery_keyboard())
            data['mes'] = mes
            await WorkListDelivery.choice_delivery.set()


@dp.callback_query_handler(state=[WorkListDelivery.choice_delivery])
async def add_delivery_work(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'exit':
        await back(callback_query, state)
    else:
        async with state.proxy() as data:
            data['delivery_id'] = callback_query.data
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=data['mes'].message_id)
            mes = await bot.send_message(callback_query.from_user.id, f'\nВыберите работу:',
                                         reply_markup=generate_works(delivery=True))
            data['mes'] = mes
            await WorkListDelivery.choice_work.set()


@dp.callback_query_handler(state=[WorkListDelivery.choice_work, WorkListDelivery.input_num])
async def add_works_delivery(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'exit':
        await back(callback_query, state)
    else:
        async with state.proxy() as data:
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=data['mes'].message_id)
            if callback_query.data == 'send':
                date = data.get('date')
                works = data.get('works')
                delivery = data.get('delivery_id')

                if not works:
                    await bot.send_message(callback_query.from_user.id, '❗️Вы ни чего не заполнил, чтобы отправлять❗️',
                                           reply_markup=menu_keyboards(callback_query.from_user.id))
                else:
                    user_id_site = User.get(User.telegram_id == callback_query.from_user.id).site_user_id
                    code = post_works(date, user_id_site, works, delivery)
                    if code == 200:
                        mes = '✅Отправленно✅'
                    elif code == 401:
                        mes = '🛑Запись на эту дату существует🛑'
                    elif code == 403:
                        mes = '❌Вы не работаете❌'
                    else:
                        mes = '☣️Возникла ошибка☣️'
                    await bot.send_message(callback_query.from_user.id, mes,
                                           reply_markup=menu_keyboards(callback_query.from_user.id))
                await state.reset_state()
                await state.finish()
            else:
                work_id = callback_query.data.split('_')
                data['current_work'] = int(work_id[1])
                await bot.send_message(callback_query.from_user.id,
                                       f'Теперь введите количество:')
                await WorkListDelivery.input_num.set()


@dp.callback_query_handler(state='*')
async def add_works_delivery(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'exit':
        await back(callback_query, state)