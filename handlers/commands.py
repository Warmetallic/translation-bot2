from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.translate_states import TranslateStates
from API.api_function import api_connect
from keyboards.inline_markup import create_language_markup, create_dates_markup
from database.db_functions import update_user
import json
from database.db_functions import (
    get_user_history,
    delete_user_history,
    get_user_history_dates,
)

router = Router()


@router.message(Command("translate"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Please choose a language to translate to:",
        reply_markup=create_language_markup(),
    )


@router.message(Command("history"))
async def show_history(message: types.Message):
    user_id = message.from_user.id
    history = await get_user_history(user_id)

    if history:
        response = "Translation History:\n\n"
        for idx, entry in enumerate(history, 1):
            original_text = entry["original_text"]
            translated_text = entry["translated_text"]
            created_at = entry["created_at"]
            response += f"{idx}. Original Text: {original_text}\nResult: {translated_text}\n{created_at}\n\n"
    else:
        response = "Translation History is empty."

    await message.answer(response)


@router.message(Command("history_dates"))
async def cmd_history_dates(message: types.Message):
    user_id = message.from_user.id
    dates = await get_user_history_dates(user_id)

    if dates:
        await message.answer(
            "Please choose a date to view the translation history:",
            reply_markup=create_dates_markup(dates),
        )
    else:
        await message.answer("No translation history found.")


@router.message(Command("delete_history"))
async def cmd_delete_history(message: types.Message):
    user_id = message.from_user.id
    deleted_count = delete_user_history(user_id)

    if deleted_count > 0:
        response = f"Deleted {deleted_count} records from your Translation History."
    else:
        response = "No records found to delete in your Translation History."

    await message.answer(response)


@router.message(TranslateStates.INPUT_TEXT)
async def translate_function(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    target_lang = user_data["target_lang"]
    user_input = message.text
    try:
        res = await api_connect(user_input, target_lang)
        if res.get("translations"):
            translated_text = res["translations"][0]["text"]
            await message.answer(
                f"{translated_text}",
                reply_markup=create_language_markup(),
            )
            update_user(message.from_user.id, user_input, translated_text)
        else:
            # Log the response for debugging
            print(f"API request failed with response: {res}")
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
