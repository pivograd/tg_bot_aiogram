
from aiogram.utils import executor

from create_bot import dp
from data_base import sqlite_db
from handlers.admin import admin_commands
from handlers.user import users_commands


sqlite_db.sql_start()
executor.start_polling(dp, skip_updates=True)