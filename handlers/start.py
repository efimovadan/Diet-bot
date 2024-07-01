from aiogram import types

async def cmd_start(message: types.Message): 
    await message.answer("Приветствую, меня зовут Питательный Помощник! Я помогу вам с вопросами о питании и здоровом образе жизни.")


