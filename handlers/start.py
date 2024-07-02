from aiogram import types
from .message_text import message_dict
from database import UserRepository
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.utils.formatting import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from nutrients import calculate_nutrients
from models import User
class Registration(StatesGroup):
    age = State()  
    height = State()  
    weight = State()  
    activity_level = State()  
    goal = State()
    gender = State()


def register_start_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command(commands="start"))
    dp.message.register(process_age, Registration.age)
    dp.message.register(process_height, Registration.height)
    
    dp.message.register(process_weight, Registration.weight)
    
    dp.callback_query.register(activity_level, Registration.activity_level, lambda c: c.data.startswith("activity_level"))
    dp.callback_query.register(process_goal, Registration.goal, lambda c: c.data.startswith("goal"))
    dp.callback_query.register(process_gender, Registration.gender, lambda c: c.data.startswith("gender"))
    

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


async def process_weight(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        weight = int(message.text)
        if weight < 0:
            await message.answer(message_dict['negative_weight'])
            return
        
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Низкий",
            callback_data="activity_level:0")
        )

        builder.add(types.InlineKeyboardButton(
            text="Средний",
            callback_data="activity_level:1")
        )

        builder.add(types.InlineKeyboardButton(
            text="Высокий",
            callback_data="activity_level:2")
        )

        if weight < 50:
            await message.answer(message_dict['light_weight'], reply_markup=builder.as_markup())
        elif weight > 100:
            await message.answer(message_dict['heavy_weight'], reply_markup=builder.as_markup())
        else:
            await message.answer(message_dict['normal_weight'], reply_markup=builder.as_markup())
        
        await state.update_data(weight=weight)
        await state.set_state(Registration.activity_level)
       
    except ValueError as e:
        print (e)
        await message.answer(message_dict['wrong_weight'])


async def activity_level(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        activity_level_data = callback_query.data.split(":")
        if len(activity_level_data) != 2:
            raise ValueError("Incorrect callback_data format")
        
        activity_level = int(activity_level_data[1])
        if activity_level not in [0, 1, 2]:
            raise ValueError("Invalid activity_level value")
        
        await state.update_data(activity_level=activity_level)

        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Похудеть",
            callback_data="goal:0")
        )

        builder.add(types.InlineKeyboardButton(
            text="Поддерживать вес",
            callback_data="goal:1")
        )

        builder.add(types.InlineKeyboardButton(
            text="Набрать вес",
            callback_data="goal:2")
        )

        await callback_query.message.answer(message_dict['goal'], reply_markup=builder.as_markup())

        await state.set_state(Registration.goal)

    except Exception as e:
        print(e)
        await callback_query.answer(message_dict['error'])

async def process_goal(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        goal = callback_query.data.split(":")
        if len(goal) != 2:
            raise ValueError("Incorrect callback_data format")
        
        goal_data = int(goal[1])
        if goal_data not in [0, 1, 2]:
            raise ValueError("Invalid goal value")
        
        await state.update_data(goal=goal_data)

        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="Мужской", callback_data="gender:male"))
        builder.add(types.InlineKeyboardButton(text="Женский", callback_data="gender:female"))
        await callback_query.message.answer(message_dict['gender'], reply_markup=builder.as_markup())
        await state.set_state(Registration.gender)
        
    except Exception as e:
        print(e)
        await callback_query.answer(message_dict['error'])


async def process_gender(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        gender_data = callback_query.data.split(":")
        if len(gender_data) != 2:
            raise ValueError("Incorrect callback_data format")

        gender = gender_data[1]
        if gender not in ["male", "female"]:
            raise ValueError("Invalid gender value")
        gender = True if gender == "male" else False
        await state.update_data(gender=gender)

        await callback_query.message.answer(message_dict['finish'])

        data = await state.get_data()
        
        user = User(
            telegram_id=callback_query.from_user.id,
            username=callback_query.from_user.username,
            height=data['height'],
            weight=data['weight'],
            age=data['age'],
            physical_activity_level=data['activity_level'],
            goal=data['goal'],
            gender=gender,
        )

        user_repository = UserRepository()
        await user_repository.create(user)

        
        nutrients = calculate_nutrients(user)
        await callback_query.message.answer(
            f"Ваша норма КБЖУ на день:\n\t\tКалории: {nutrients['calories']}, "
            f"\n\t\tБелки: {nutrients['proteins']} г,\n\t\tЖиры: {nutrients['fats']} г, "
            f"\n\t\tУглеводы: {nutrients['carbs']} г.\n\n"
        )

        callback_query.answer()
        await state.clear() 

    except Exception as e:
        print(e)
        await callback_query.answer(message_dict['error'])