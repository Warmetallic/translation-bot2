import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from handlers import commands, callbacks
from database.db_functions import create_db
from bot_instance import bot

# Getting secret keys from decouple
bot_key = config("BOT_KEY")

# Initialize the Bot with DefaultBotProperties for default settings
dp = Dispatcher(storage=MemoryStorage())

# Include routers
dp.include_router(commands.router)
dp.include_router(callbacks.router)


# Main function to start polling
async def main():
    try:
        await create_db()
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        print("Polling cancelled.")
    finally:
        # Perform cleanup actions here
        await bot.session.close()
        print("Bot session closed.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped manually.")
