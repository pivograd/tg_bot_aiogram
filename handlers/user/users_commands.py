from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from create_bot import bot, dp
from data_base.sqlite_db import sql_specificity_is_empty, sql_get_text_anecdote, sql_get_specifications_list
from different_checks.message_checks import message_in_list
from handlers.user.settings import message_dict, get_random_title
from keyboards.default.admin_kb import get_keyboard_with_title_specificity, get_specificatoins_keyboard
from keyboards.default.users_kb import button_case_users
from states.user.user_states import ChoosingAnAnecdoteState


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Здесь будет список доступных команд', reply_markup=button_case_users)
        await message.delete()
    except:
        await message.answer('Надо в личку написать-__- \nhttps://t.me/OP_tg_bot')
        await message.delete()

@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
@dp.message_handler(state="*", commands='Отмена')
async def cancel_handler(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК', reply_markup=button_case_users)

@dp.message_handler(Text(equals='Анекдоты', ignore_case=True))
@dp.message_handler(commands=['Анекдоты'], state=None)
async def get_specificity_anecdote(message: types.Message):
    kb_specificity = await get_specificatoins_keyboard()
    await ChoosingAnAnecdoteState.st_choosing_title.set()
    await bot.send_message(message.from_user.id, 'Выбери интересующую тему', reply_markup=kb_specificity)

@dp.message_handler(state=ChoosingAnAnecdoteState.st_choosing_title)
async def get_titles_by_specificity(message: types.Message, state: FSMContext):
    specificity_list = await sql_get_specifications_list()
    kb_specificity = await get_specificatoins_keyboard()
    try:
        await message_in_list(message.text, specificity_list)
        await ChoosingAnAnecdoteState.next()
        kb = await get_keyboard_with_title_specificity(message.text)
        if await sql_specificity_is_empty(data=message.text):
            raise ValueError
        await message.reply('Выберите название', reply_markup=kb)
        async with state.proxy() as data:
            data['specificity'] = message.text
    except NameError:
        await message.reply('Такой темы нет, выберите тему из предложенных', reply_markup=kb_specificity)
    except ValueError:
        await message.reply('К сожалению анекдотов по этой теме ещё нет(', reply_markup=button_case_users)
        await state.finish()

@dp.message_handler(state=ChoosingAnAnecdoteState.st_get_text)
async def get_anecdote_text(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        kb = await get_keyboard_with_title_specificity(message=data['specificity'])
    try:
        text_anecdote = await sql_get_text_anecdote(message.text)
        await bot.send_message(message.from_user.id, text=text_anecdote[0][0], reply_markup=button_case_users)
        await state.finish()
    except NameError:
        await message.reply('Такого анекдота нет, попробуйте ещё.\n Выберите анекдот из спиcка', reply_markup=kb)

@dp.message_handler(Text(equals='Случайный анекдот', ignore_case=True))
@dp.message_handler(commands=['Случайный_анекдот'])
async def get_random_anecdote(message: types.Message):
    random_t = await get_random_title()
    text_random_anecdote = await sql_get_text_anecdote(random_t[0])
    text_output = f'Рандомный анекдот с названием "{random_t[0]}" :\n\n{text_random_anecdote[0][0]}'
    await bot.send_message(message.from_user.id, text=text_output)




@dp.message_handler()
async def echo_send(message : types.Message):
    """"Отвечаем на слова триггеры из словаря. Ключ = слово, Значение = ответ"""
    for mes in message_dict.keys():
        if mes in message.text.lower():
            await message.answer(message_dict[mes], reply_markup=button_case_users)
            break
