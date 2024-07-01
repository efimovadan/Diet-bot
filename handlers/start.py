from aiogram import types
from message_text import message_dict

async def cmd_start(message: types.Message): 
    await message.answer(message_dict['welcome'])



