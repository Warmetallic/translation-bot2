from aiogram.fsm.state import StatesGroup, State


class TranslateStates(StatesGroup):
    CHOOSE_LANGUAGE = State()
    INPUT_TEXT = State()
    CHOOSE_FILE_LANGUAGE = State()
    UPLOAD_DOCUMENT = State()
