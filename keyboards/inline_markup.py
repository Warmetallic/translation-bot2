from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class LanguageCallbackData(CallbackData, prefix="lang"):
    language: str


class DateCallbackData(CallbackData, prefix="date"):
    date: str


def create_language_markup():
    bt1 = InlineKeyboardButton(
        text="РУ 🇷🇺", callback_data=LanguageCallbackData(language="RU").pack()
    )
    bt2 = InlineKeyboardButton(
        text="ENG 🇬🇧", callback_data=LanguageCallbackData(language="EN").pack()
    )
    markup = InlineKeyboardMarkup(inline_keyboard=[[bt1, bt2]])
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
