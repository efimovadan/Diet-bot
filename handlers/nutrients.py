from aiogram import Dispatcher
from aiogram.filters.command import Command
from .message_text import message_dict
from aiogram import types
from database import UserRepository
from nutrients import calculate_nutrients

def register_nutrients_handlers(dp: Dispatcher):
    dp.message.register(cmd_daily, Command(commands="daily"))


async def cmd_daily(message: types.Message):
    user_repository = UserRepository()
    user = await user_repository.get_user(message.from_user.id)
    if not user:
        await message.answer(message_dict['not_registered'])
        return
    nutrients = calculate_nutrients(user)
    await message.answer(
        f"Ваша норма КБЖУ на день:\n\t\tКалории: {nutrients['calories']}, "
        f"\n\t\tБелки: {nutrients['proteins']} г,\n\t\tЖиры: {nutrients['fats']} г, "
        f"\n\t\tУглеводы: {nutrients['carbs']} г.\n\n")
