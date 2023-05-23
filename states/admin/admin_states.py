from aiogram.dispatcher.filters.state import StatesGroup, State


class LoadAnecdoteState(StatesGroup):

    st_title = State()
    st_text = State()
    st_specificity = State()
    st_new_specificity = State()


class DeleteAnecdoteState(StatesGroup):

    st_specificity_d = State()
    st_title_d = State()


class DeleteSpecificity(StatesGroup):

    st_delete_specificity = State()


class AddSpecificity(StatesGroup):

    st_add_specificity = State()