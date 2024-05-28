from aiogram import types, Router

from actions import main_action
from texts.maintext import any_answer

action_handler_router = Router()

@action_handler_router.message()
async def data_action(message: types.Message):
    try:
        data = eval(message.text)
        dt_from = data["dt_from"]
        dt_upto = data["dt_upto"]
        group_type = data["group_type"]
        answer = main_action.aggregatedb_bygroup(dt_from, dt_upto, group_type)
        await message.answer(f'{answer}')
    except KeyError:
        await message.answer(any_answer)
    except ValueError:
        await message.answer(any_answer)
    except TypeError:
        await message.answer(any_answer)
    except IndentationError:
        await message.answer(any_answer)
    except SyntaxError:
        await message.answer(any_answer)