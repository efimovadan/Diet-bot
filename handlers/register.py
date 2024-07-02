from aiogram import Dispatcher
from aiogram.filters.command import Command

from handlers.start import register_start_handlers
from handlers.help import register_help
from handlers.nutrients import register_nutrients_handlers
def register_handlers(dp: Dispatcher):
    register_start_handlers(dp)
    register_help(dp)
    register_nutrients_handlers(dp)
    
    
