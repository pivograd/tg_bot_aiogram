from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_delete = InlineKeyboardMarkup(row_width=1)

btnn_delete_specificity = InlineKeyboardButton('Удалить тему', callback_data='delete_specificity')

ikb_delete.add(btnn_delete_specificity)

ikb_add = InlineKeyboardMarkup(row_width=1)

btnn_add_specificity = InlineKeyboardButton('Добавить тему', callback_data='add_specificity')

ikb_add.add(btnn_add_specificity)

