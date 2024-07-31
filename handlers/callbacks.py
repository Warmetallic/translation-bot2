from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType
from aiogram.handlers import MessageHandler
from states.translate_states import TranslateStates
from API.api_function import api_connect_document
from database.db_functions import get_user_history_by_date
from bot_instance import bot

router = Router()


class LanguageCallbackData(CallbackData, prefix="lang"):
    language: str


class FileLanguageCallbackData(CallbackData, prefix="file_lang"):
    language: str


class DateCallbackData(CallbackData, prefix="date"):
    date: str


@router.callback_query(LanguageCallbackData.filter())
async def process_language(
    callback_query: types.CallbackQuery,
    callback_data: LanguageCallbackData,
    state: FSMContext,
):
    target_lang = callback_data.language
    await state.update_data(target_lang=target_lang)
    await state.set_state(TranslateStates.INPUT_TEXT)
    await callback_query.message.answer("Please enter the text to translate:")


@router.callback_query(DateCallbackData.filter())
async def process_date_selection(
    callback_query: types.CallbackQuery,
    callback_data: DateCallbackData,
    state: FSMContext,
):
    user_id = callback_query.from_user.id
    selected_date = callback_data.date

    history = await get_user_history_by_date(user_id, selected_date)

    if history:
        response = f"Translation History for {selected_date}:\n\n"
        for idx, entry in enumerate(history, 1):
            original_text = entry["original_text"]
            translated_text = entry["translated_text"]
            created_at = entry["created_at"]
            response += f"{idx}. Original Text: {original_text}\nResult: {translated_text}\n{created_at}\n\n"
    else:
        response = f"No translation history found for {selected_date}."

    await callback_query.message.answer(response)
    await callback_query.answer()


@router.callback_query(FileLanguageCallbackData.filter())
async def process_file_language(
    callback_query: types.CallbackQuery,
    callback_data: FileLanguageCallbackData,
    state: FSMContext,
):
    target_lang = callback_data.language
    await state.update_data(target_lang=target_lang)
    await callback_query.message.answer("Please upload the document to translate.")
    await state.set_state(TranslateStates.UPLOAD_DOCUMENT)
