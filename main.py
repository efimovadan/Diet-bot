import asyncio
import logging
from config import Config
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from database import Database, UserRepository
from handlers import register_handlers

async def cmd_dice(message: types.Message):
	await message.answer_dice()
     
async def main():
    config = Config()
    bot = Bot(token=config['token'])
    dp = Dispatcher()
    
    # TODO: вынести инициализацию синглтонов
    await Database.initialize(config['db'])
    
    logging.basicConfig(level=logging.DEBUG)# TODO: Вынести в конфиг
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
