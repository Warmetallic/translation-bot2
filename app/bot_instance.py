# bot_instance.py
from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config

# Getting secret keys from decouple
bot_key = config("BOT_KEY")

# Initialize the Bot with DefaultBotProperties for default settings
bot = Bot(token=bot_key, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
