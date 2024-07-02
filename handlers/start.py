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
    # dp.message.register(process_height, state=Registration.height)
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
        if age < 20:
            await message.answer(message_dict['young_age'])
        elif age > 50:
            await message.answer(message_dict['old_age'])
        else:
            await message.answer(message_dict['normal_age'])
        async with state.proxy() as data:
            data['age'] = age
        await Registration.next()
    except ValueError:
        await message.answer(message_dict['wrong_age'])

