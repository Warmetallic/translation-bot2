from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from states.translate_states import TranslateStates

router = Router()


@router.callback_query()
async def process_language(callback_query: types.CallbackQuery, state: FSMContext):
    target_lang = callback_query.data
    await state.update_data(target_lang=target_lang)
    await state.set_state(TranslateStates.INPUT_TEXT)
    await callback_query.message.answer("Please enter the text to translate:")
