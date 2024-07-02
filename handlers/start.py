from aiogram import types
from .message_text import message_dict
from database import UserRepository
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher
from aiogram.filters import Command
class Registration(StatesGroup):
    age = State()  
    height = State()  
    weight = State()  
    activity_level = State()  
    goal = State()  


def register_start_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command(commands="start"))
    dp.message.register(process_age, Registration.age)
    dp.message.register(process_height, Registration.height)
    
    # dp.message.register(process_weight, state=Registration.weight)
    # dp.message.register(process_activity_level, state=Registration.activity_level)
    # dp.message.register(process_goal, state=Registration.goal)

async def cmd_start(message: types.Message, state: FSMContext): 
    user_repository = UserRepository()
    exist = await user_repository.is_exist(message.from_user.id)
    if not exist:
        await state.set_state(Registration.age)
        await message.answer(message_dict['welcome'])
    else:
        await message.answer(message_dict['already_registered'])    


async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age < 0:
            await message.answer(message_dict['negative_age'])
            return
        if age < 20:
            await message.answer(message_dict['young_age'])
        elif age > 50:
            await message.answer(message_dict['old_age'])
        else:
            await message.answer(message_dict['normal_age'])
        await state.update_data(age=age)
        await state.set_state(Registration.height)

    except ValueError:
        await message.answer(message_dict['wrong_age'])


async def process_height(message: types.Message, state: FSMContext):
    try:
        height = int(message.text)
        if height < 0:
            await message.answer(message_dict['negative_height'])
            return
        if height < 150:
            await message.answer(message_dict['short_height'])
        elif height > 200:
            await message.answer(message_dict['tall_height'])
        else:
            await message.answer(message_dict['normal_height'])
        
        await state.update_data(height=height)
        await state.set_state(Registration.weight)
    except ValueError:
        await message.answer(message_dict['wrong_height'])
