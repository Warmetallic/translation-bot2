from aiogram.fsm.state import StatesGroup, State


class TranslateStates(StatesGroup):
    CHOOSE_LANGUAGE = State()
    INPUT_TEXT = State()
