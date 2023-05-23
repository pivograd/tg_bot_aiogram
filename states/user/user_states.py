from aiogram.dispatcher.filters.state import StatesGroup, State


class ChoosingAnAnecdoteState(StatesGroup):

    st_choosing_title = State()
    st_get_text = State()