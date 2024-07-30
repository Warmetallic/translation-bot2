from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_language_markup():
    bt1 = InlineKeyboardButton(text="РУ 🇷🇺", callback_data="RU")
    bt2 = InlineKeyboardButton(text="ENG 🇬🇧", callback_data="EN")
    markup = InlineKeyboardMarkup(inline_keyboard=[[bt1, bt2]])
    return markup
