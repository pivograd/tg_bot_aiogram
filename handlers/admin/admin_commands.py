from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from filters.is_admin import AdminFilter
from create_bot import dp, bot
from data_base import sqlite_db
from different_checks.message_checks import message_in_list
from keyboards.default import admin_kb
from keyboards.default.admin_kb import get_specificatoins_keyboard, get_keyboard_with_title_specificity, button_case_admin, cancel_kb
from keyboards.inline.admin_ikb import ikb_delete, ikb_add
from states.admin.admin_states import DeleteAnecdoteState, LoadAnecdoteState, DeleteSpecificity, AddSpecificity


@dp.message_handler(commands=['admin'])
async def make_changes_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Что надо?', reply_markup=admin_kb.button_case_admin)
    await message.delete()

@dp.message_handler(Text(equals='Удалить', ignore_case=True))
@dp.message_handler(commands='Удалить', state=None)
async def get_specificity_for_delete(message: types.Message):
    kb_specificity = await get_specificatoins_keyboard()
    admin_filter = AdminFilter(is_admin=True)
    if await admin_filter.check(message):
        await DeleteAnecdoteState.st_specificity_d.set()
        await message.reply('Выберите тему из которой необходимо удалить анекдот', reply_markup=kb_specificity)
        await bot.send_message(message.from_user.id, 'Удалить не нужную тему', reply_markup=ikb_delete)
    else:
        await message.reply('У вас недостаточно прав для использование этой команды')

@dp.callback_query_handler(text="delete_specificity", state='*')
async def wish_delete_specificity(call: types.CallbackQuery):
    message = call.message
    await message.delete()
    kb_specificity = await get_specificatoins_keyboard()
    await call.message.answer('Выберите тему которую хотите удалить', reply_markup=kb_specificity)
    await DeleteSpecificity.st_delete_specificity.set()

@dp.message_handler(Text(equals='удалить тему', ignore_case=True), state='*')
async def wish_delete_specificity_(message: types.Message):
    kb_specificity = await get_specificatoins_keyboard()
    await message.answer('Выберите тему которую хотите удалить', reply_markup=kb_specificity)
    await DeleteSpecificity.st_delete_specificity.set()


@dp.message_handler(Text(equals='Загрузить', ignore_case=True))
@dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    admin_filter = AdminFilter(is_admin=True)
    if await admin_filter.check(message):
        await LoadAnecdoteState.st_title.set()
        await message.reply('Введите название анекдота', reply_markup=cancel_kb)
    else:
        await message.reply('У вас недостаточно прав для использование этой команды')

@dp.callback_query_handler(text="add_specificity", state="*")
async def wish_delete_specificity(call: types.CallbackQuery):
    message = call.message
    await message.delete()
    await call.message.answer('Введите название темы')
    await LoadAnecdoteState.st_new_specificity.set()

@dp.message_handler(Text(equals='добавить тему', ignore_case=True), state='*')
async def wish_delete_specificity_(message: types.Message):
    await message.reply('Введите название темы')
    await AddSpecificity.st_add_specificity.set()

@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
@dp.message_handler(state="*", commands='Отмена')
async def cancel_handler(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК', reply_markup=admin_kb.button_case_admin)

@dp.message_handler(state=DeleteAnecdoteState.st_specificity_d)
async def get_title_for_delete_anecdote(message: types.Message, state: FSMContext):
    kb_specificity = await get_specificatoins_keyboard()
    specificity_list = await sqlite_db.sql_get_specifications_list()
    try:
        await message_in_list(message.text, specificity_list)
        await DeleteAnecdoteState.st_title_d.set()
        kb = await get_keyboard_with_title_specificity(message.text)
        if await sqlite_db.sql_specificity_is_empty(data=message.text):
            raise ValueError
        await message.reply('Выберите название', reply_markup=kb)
        async with state.proxy() as data:
            data['specificity'] = message.text
    except NameError:
        await message.reply('Такой темы нет, выберите тему из предложенных', reply_markup=kb_specificity)
    except ValueError:
        await message.reply('К сожалению в этой теме анекдотов нет', reply_markup=button_case_admin)
        await state.finish()

@dp.message_handler(state=DeleteAnecdoteState.st_title_d)
async def delete_anecdote(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        kb = await get_keyboard_with_title_specificity(message=data['specificity'])
    try:
        await sqlite_db.sql_delete_joke(message.text)
        await message.reply("Анекдот удалён из базы", reply_markup=admin_kb.button_case_admin)
        await state.finish()
    except NameError:
        await message.reply('Такого анекдота нет, попробуйте ещё.\n Выберите анекдот из спиcка', reply_markup=kb)


@dp.message_handler(state=LoadAnecdoteState.st_title)
async def load_text(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['title'] = message.text
    await LoadAnecdoteState.st_text.set()
    await message.reply("Теперь напиши текст", reply_markup=cancel_kb)


@dp.message_handler(state=LoadAnecdoteState.st_text)
async def load_specificity(message: types.Message, state: FSMContext):
    kb_specificity = await get_specificatoins_keyboard()

    async with state.proxy() as data:
        data['text'] = message.text
    await LoadAnecdoteState.st_specificity.set()
    await message.reply('Теперь выбери тему анекдота', reply_markup=kb_specificity)
    await bot.send_message(message.from_user.id, 'Добавить новую тему', reply_markup=ikb_add)

@dp.message_handler(state=LoadAnecdoteState.st_specificity)
async def load_anecdote(message: types.Message, state: FSMContext):
    kb_specificity = await get_specificatoins_keyboard()
    specificity_list = await sqlite_db.sql_get_specifications_list()
    try:
        await message_in_list(message=message.text, list=specificity_list)
        async with state.proxy() as data:
            data['specificity'] = message.text
        await sqlite_db.sql_add_joke(state)
        await message.reply("Анекдот добавлен в базу", reply_markup=admin_kb.button_case_admin)
        await state.finish()

    except:
        await message.reply('Такой тематики нет, нужно выбрать из предложенных', reply_markup=kb_specificity)

@dp.message_handler(state=LoadAnecdoteState.st_new_specificity)
async def load_anecdote_new_specificity(message: types.Message, state: FSMContext):
    try:
        await sqlite_db.sql_add_specificity(message.text)
        async with state.proxy() as data:
            data['specificity'] = message.text
        await sqlite_db.sql_add_joke(state)
        await message.reply("Тема и анекдот добавлены в базу", reply_markup=admin_kb.button_case_admin)
        await state.finish()
    except ValueError:
        await message.reply('Такая тема уже есть')

@dp.message_handler(state=DeleteSpecificity.st_delete_specificity)
async def choose_and_delete_specificity(message: types.Message, state: FSMContext):
    try:
        await sqlite_db.sql_delete_specificity(message.text)
        await message.reply('Тема удалена', reply_markup=button_case_admin)
        await state.finish()
    except ValueError:
        await message.reply('Для удаления темы в ней не должно быть анекдотов', reply_markup=button_case_admin)
        await state.finish()



@dp.message_handler(state=AddSpecificity.st_add_specificity)
async def choose_and_delete_specificity(message: types.Message, state: FSMContext):
    try:
        await sqlite_db.sql_add_specificity(message.text)
        await message.reply('Тема добавлена', reply_markup=button_case_admin)
        await state.finish()
    except ValueError:
        await message.reply('Такая тема уже есть')
        await state.finish()
