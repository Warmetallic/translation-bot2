from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class LanguageCallbackData(CallbackData, prefix="lang"):
    language: str


class DateCallbackData(CallbackData, prefix="date"):
    date: str


class FileLanguageCallbackData(CallbackData, prefix="file_lang"):
    language: str


def create_language_markup():
    languages = {
        "RU": "🇷🇺 RU",
        "EN": "🇬🇧 EN",
        "ES": "🇪🇸 ES",
        "FR": "🇫🇷 FR",
        "DE": "🇩🇪 DE",
        "ZH": "🇨🇳 ZH",
    }
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=languages[lang],
                callback_data=LanguageCallbackData(language=lang).pack(),
            )
            for lang in list(languages.keys())[i : i + 3]  # Adjust to create two rows
        ]
        for i in range(0, len(languages), 3)
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return markup


def create_file_language_markup():
    file_languages = {
        "RU": "🇷🇺 Russian",
        "EN": "🇬🇧 English",
        "ES": "🇪🇸 Spanish",
        "FR": "🇫🇷 French",
        "DE": "🇩🇪 German",
        "ZH": "🇨🇳 Chinese",
    }
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=file_languages[lang],
                callback_data=FileLanguageCallbackData(language=lang).pack(),
            )
            for lang in list(file_languages.keys())[i : i + 3]  # Adjust to create rows
        ]
        for i in range(0, len(file_languages), 3)
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return markup


def create_dates_markup(dates):
    inline_keyboard = []
    for date in dates:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=date, callback_data=DateCallbackData(date=date).pack()
                )
            ]
        )
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return markup
