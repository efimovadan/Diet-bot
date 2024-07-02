from aiogram import types
from .message_text import message_dict
from database import UserRepository

class RegisterStates(StatesGroup):
    

async def cmd_start(message: types.Message): 
    user_repository = UserRepository()
    await message.answer(message_dict['welcome'])
    
    exist = await user_repository.is_exist(message.from_user.id)
    if not exist:
        await message.answer("You are not registered!")
    else:
        await message.answer(message_dict['already_registered'])    


