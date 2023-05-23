from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_anecdotes = KeyboardButton('Анекдоты')
button_cancel = KeyboardButton('/Отмена')
button_random_anecdote = KeyboardButton('Случайный анекдот')

button_case_users = ReplyKeyboardMarkup(resize_keyboard=True).add(button_anecdotes).add(button_random_anecdote)