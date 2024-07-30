from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.translate_states import TranslateStates
from API.api_function import api_connect
from keyboards.inline_markup import create_language_markup
from database.db_functions import update_user
import json

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Please choose a language to translate to:",
        reply_markup=create_language_markup(),
    )


@router.message(Command("delete_history"))
async def cmd_delete_history(message: types.Message):
    # Implementation for deleting history ...
    pass


@router.message(TranslateStates.INPUT_TEXT)
async def translate_function(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    target_lang = user_data["target_lang"]
    user_input = message.text
    try:
        res = api_connect(user_input, target_lang)
        if res.status_code == 200:
            data = json.loads(res.text)
            translated_text = data["translations"][0]["text"]
            await message.answer(
                f"{translated_text}",
                reply_markup=create_language_markup(),
            )
            update_user(message.from_user.id, user_input, translated_text)
        else:
            # Log the response for debugging
            print(f"API request failed with status code: {res.status_code}")
            print(f"Response text: {res.text}")
            await message.answer("Translation failed. Please try again later.")
    except Exception as e:
        # Log the exception
        print(f"An error occurred: {e}")
        await message.answer("An error occurred. Please try again later.")
    finally:
        await state.clear()  # Ensure the state is cleared after processing
        await state.set_state(
            TranslateStates.CHOOSE_LANGUAGE
        )  # Reset state to choose language
