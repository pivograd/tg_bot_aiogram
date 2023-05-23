from data_base.sqlite_db import sql_get_all_titles
from random import randint


message_dict = {
    'приветик': 'Пукни в пакетик...', 'привет': 'И тебе привет!',
    'здорова': 'Даров бродяга', 'Соня крутая?' : 'Гош? - ДА!'


}

async def get_random_title():

    all_titles = await sql_get_all_titles()
    random_number = randint(0, len(all_titles)-1)
    random_title = all_titles[random_number]
    return random_title