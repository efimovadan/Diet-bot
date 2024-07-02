from aiogram import types, Dispatcher
from aiogram.filters.command import Command
from .message_text import message_dict

def register_help(dp: Dispatcher):
    dp.message.register(cmd_help, Command(commands="help"))

async def cmd_help(message: types.Message):
    await message.answer(message_dict['help'])
