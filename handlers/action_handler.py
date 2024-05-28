from aiogram import F, types, Router

from actions import main_action
from texts.maintext import any_answer

action_handler_router = Router()

@action_handler_router.message(F.text.startswith('{'),
                               F.text.endsswith('}'))
async def start_cmd(message: types.Message):
    data = message.text
    dt_from = data["dt_from"]
    dt_upto = data["dt_from"]
    group_type = data["group_type"]
    answer = main_action.aggregatedb_bygroup(dt_from, dt_upto, group_type)
    await message.answer(f'{answer}')

@action_handler_router.message()
async def start_cmd(message: types.Message):
    await message.answer(any_answer)