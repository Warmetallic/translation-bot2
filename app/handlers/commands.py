from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram import types
from aiogram.types import FSInputFile
from utils.rabbitmq import publish_message
import os
from aiogram.fsm.context import FSMContext
from states.translate_states import TranslateStates
import asyncio
from API.api_function import (
    api_connect,
    api_connect_document,
    download_translated_document,
    check_translation_status,
)
from keyboards.inline_markup import (
    create_language_markup,
    create_dates_markup,
    create_file_language_markup,
)
import json
from database.db_functions import (
    get_user_history,
    delete_user_history,
    get_user_history_dates,
    update_user,
)
from bot_instance import bot


DOWNLOADS_FOLDER = os.path.join("app", "downloads")

router = Router()


@router.message(Command("translate"))
async def translate(message: types.Message):
    publish_message("translate_queue", message.text)
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
async def history_dates(message: types.Message):
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
async def delete_history(message: types.Message):
    user_id = message.from_user.id
    deleted_count = await delete_user_history(user_id)

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
            await update_user(message.from_user.id, user_input, translated_text)
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


@router.message(Command("translate_file"))
async def translate_file(message: types.Message, state: FSMContext):
    await message.answer(
        "Please choose a language to translate the document to:",
        reply_markup=create_file_language_markup(),
    )
    await state.set_state(TranslateStates.CHOOSE_FILE_LANGUAGE)


async def send_translated_document(user_id: int, file_path: str):
    """Send the translated document to the user."""
    try:
        # Create an InputFile instance with the file path
        input_file = FSInputFile(file_path)
        await bot.send_document(chat_id=user_id, document=input_file)
        print(f"Document sent to user {user_id}")
    except Exception as e:
        print(f"Failed to send document: {e}")


@router.message(TranslateStates.UPLOAD_DOCUMENT)
async def handle_document_upload(message: types.Message, state: FSMContext):
    try:
        document = message.document
        if not document:
            await message.answer("No document found. Please upload a valid document.")
            return

        file_path = os.path.join(DOWNLOADS_FOLDER, document.file_name)
        file_info = await bot.get_file(document.file_id)
        file_path_telegram = file_info.file_path

        try:
            os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)
            await bot.download_file(file_path_telegram, file_path)
            await message.answer(f"Document saved to {file_path}")
        except Exception as e:
            print(f"Failed to download file: {e}")
            await message.answer("An error occurred while downloading the document.")
            return

        data = await state.get_data()
        target_lang = data.get("target_lang")
        if not target_lang:
            await message.answer("Target language not specified. Please try again.")
            return

        translation_response = await api_connect_document(file_path, target_lang)
        if "error" in translation_response:
            await message.answer("Failed to translate the document. Please try again.")
            return

        document_id = translation_response.get("document_id")
        document_key = translation_response.get("document_key")

        # Poll the document status until the translation is complete
        while True:
            status_response = await check_translation_status(document_id, document_key)
            status = status_response.get("status")

            if status == "completed" or status == "done":
                break
            elif "error" in status_response:
                await message.answer(
                    "Error checking document status. Please try again."
                )
                return

            await asyncio.sleep(10)  # Wait before polling again

        # Download the translated document
        output_path = os.path.join(DOWNLOADS_FOLDER, f"translated_{document.file_name}")
        download_response = await download_translated_document(
            document_id, document_key, output_path
        )
        if "error" in download_response:
            await message.answer(
                "Failed to download the translated document. Please try again."
            )
        else:
            await send_translated_document(message.from_user.id, output_path)
            await message.answer("Here is your translated document.")
            await state.clear()

    except Exception as e:
        print(f"Error handling document upload: {e}")
        await message.answer("An error occurred while handling the document.")
    finally:
        await state.clear()
