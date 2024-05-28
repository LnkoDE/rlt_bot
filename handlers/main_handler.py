from aiogram import types, Router
from aiogram.filters import CommandStart, Command

from texts.maintext import start_text, help_text

main_handler_router = Router()

@main_handler_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(start_text)

@main_handler_router.message(Command('help'))
async def start_cmd(message: types.Message):
    await message.answer(help_text)
