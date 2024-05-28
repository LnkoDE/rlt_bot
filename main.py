import asyncio
import os

from aiogram import Bot, Dispatcher

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.main_handler import main_handler_router
from handlers.action_handler import action_handler_router

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_routers(
    main_handler_router,
)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())