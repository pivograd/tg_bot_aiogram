from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data_base.sqlite_db import cur, sql_get_specifications_list


button_load = KeyboardButton('Загрузить')
button_delete = KeyboardButton('Удалить')
button_anecdotes = KeyboardButton('Анекдоты')
button_cancel = KeyboardButton('/Отмена')
button_random_anecdote = KeyboardButton('Случайный анекдот')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load)\
			.add(button_delete).add(button_anecdotes).add(button_random_anecdote)

cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)

async def get_specificatoins_keyboard():
    kb_specificity = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for specificity in await sql_get_specifications_list():
        kb_specificity.insert(KeyboardButton(specificity))
    kb_specificity.add(button_cancel)

    return kb_specificity

async def get_keyboard_with_title_specificity(message):
    test_kb_3 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for name in cur.execute('SELECT title FROM Anecdotes WHERE specificity = ?', [message]).fetchall():

        button_anecdote = KeyboardButton(name[0])
        test_kb_3.insert(button_anecdote)
    test_kb_3.add(button_cancel)

    return test_kb_3