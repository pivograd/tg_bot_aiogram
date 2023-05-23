import sqlite3 as sq

base = sq.connect('op_bot_database.db')
cur = base.cursor()

def sql_start():
    global base, cur
    base = sq.connect('op_bot_database.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.commit()

async def sql_add_joke(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO Anecdotes VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_delete_joke(data):
    title_joke = cur.execute('SELECT title FROM Anecdotes WHERE title == ?', (data,)).fetchall()
    if title_joke:
        cur.execute('DELETE FROM Anecdotes WHERE title == ?', (data,))
        base.commit()
    else:
        raise NameError

async def sql_get_text_anecdote(data):
    text_anecdote = cur.execute('SELECT text FROM Anecdotes WHERE title == ?', [data]).fetchall()
    if text_anecdote:
        return text_anecdote
    else:
        raise NameError

async def sql_specificity_is_empty(data):
    titles = cur.execute('SELECT title FROM Anecdotes WHERE specificity == ?', [data]).fetchall()
    if titles:
        return False
    else:
        return True

async def sql_get_all_titles():
    titles = cur.execute('SELECT title FROM Anecdotes').fetchall()
    return titles

async def sql_get_specifications_list():
    specifications = cur.execute('SELECT specificity FROM specifications').fetchall()
    res = [elem[0] for elem in specifications]
    return res

async def sql_delete_specificity(data):
    anecdotes_in_specificity = cur.execute('SELECT title FROM Anecdotes WHERE specificity == ?', (data,)).fetchall()
    if anecdotes_in_specificity:
        raise ValueError
    else:
        cur.execute('DELETE FROM specifications WHERE specificity == ?', (data,))
        base.commit()


async def sql_add_specificity(data):
    same_specification = cur.execute('SELECT specificity FROM specifications WHERE specificity == ?', [data]).fetchall()
    if same_specification:
        raise ValueError
    else:
        cur.execute('INSERT INTO specifications VALUES (?)', (data,))
        base.commit()
