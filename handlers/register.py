from aiogram import Dispatcher
from aiogram.filters.command import Command

from handlers.start import register_start_handlers

def register_handlers(dp: Dispatcher):
    register_start_handlers(dp)
    
