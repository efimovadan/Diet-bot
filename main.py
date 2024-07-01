import asyncio
import logging
from config import Config
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

# Хэндлер на команду /start
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

async def cmd_dice(message: types.Message):
	await message.answer_dice()
     
async def main():
    
    config = Config()
    bot = Bot(token=config['token'])
    dp = Dispatcher()
    logging.basicConfig(level=logging.DEBUG)# TODO: Вынести в конфиг
    dp.message.register(Command("start"), cmd_start)
    dp.message.register(Command("dice"), cmd_dice)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())