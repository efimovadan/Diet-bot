import asyncio
import logging
from config import Config
from aiogram import Bot, Dispatcher, types
from database import Database
from handlers import register_handlers


async def cmd_dice(message: types.Message):
	await message.answer_dice()
     
async def main():
    config = Config()
    bot = Bot(token=config['token'])
    dp = Dispatcher()

    await Database.initialize(config['db'])
    
    logging.basicConfig(level=logging.DEBUG)# TODO: Вынести в конфиг
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
