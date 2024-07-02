from aiogram import Dispatcher
from aiogram.filters.command import Command

from handlers.start import cmd_start

def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    
