from aiogram import Dispatcher
from aiogram.filters.command import Command
from .message_text import message_dict
from aiogram import types
from database import UserRepository, ProductRepository
from nutrients import calculate_nutrients, calculate_daily_diet



def register_nutrients_handlers(dp: Dispatcher):
    dp.message.register(cmd_daily, Command(commands="daily"))
    dp.message.register(cmd_product, Command(commands="product"))
    dp.message.register(cmd_diet, Command(commands="diet"))
    dp.message.register(cmd_diet_list, Command(commands="diet_list"))
    dp.message.register(cmd_calculate_nutrients, Command(commands="calculate_nutrients"))


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
    
async def cmd_product(message: types.Message):
    parts = message.text.split()
    products_names = []
    matched_products = []

    if len(parts) > 1:
        products_names = [part.lower() for part in parts[1:]]

    product_repo = ProductRepository()

    matched_products = await product_repo.get_products_by_names(products_names)

    if matched_products:
        response = "Найденные продукты:\n\n" + "\n\n".join([
            f"{product.name}: \n\t\t{product.calories} Ккал."
            f"\n\t\tБелки: {product.proteins} г.\n\t\tЖиры: {product.fats} г.\n\t\tУглеводы: {product.carbs} г."
            for product in matched_products
        ])
    else:
        response = "Продукты не найдены."

    await message.reply(response)

async def cmd_diet(message: types.Message):
    user_repository = UserRepository()
    user = await user_repository.get_user(message.from_user.id)
    if not user:
        await message.answer(message_dict['not_registered'])
        return

    diet_plan = await calculate_daily_diet(user)
    if diet_plan:
        response = "Ваш план питания на день:\n\n" + "\n\n".join([
            f"{product_name}: {grams} грамм" for product_name, grams in diet_plan
        ])
    else:
        response = "Не удалось составить диету."

    await message.answer(response)

async def cmd_diet_list(message: types.Message):
    parts = message.text.split()
    products_names = []
    if len(parts) > 1:
        products_names = [part.lower() for part in parts[1:]]

    user_repository = UserRepository()
    user = await user_repository.get_user(message.from_user.id)
    if not user:
        await message.answer(message_dict['not_registered'])
        return

    product_repo = ProductRepository()
    matched_products = await product_repo.get_products_by_names(products_names)
    if not matched_products:
        await message.answer("Указанные продукты не найдены.")
        return

    diet_plan = await calculate_daily_diet(user, products_names)
    if diet_plan:
        response = "Ваш план питания на день:\n\n" + "\n\n".join([
            f"{product_name}: {grams} грамм" for product_name, grams in diet_plan
        ])
    else:
        response = "Не удалось составить диету."
    
    await message.answer(response)

import re
async def cmd_calculate_nutrients(message: types.Message):
    text = message.text
    pattern = r"(\w+)\s+(\d+)\s*гр"
    items = re.findall(pattern, text, re.IGNORECASE)

    product_repo = ProductRepository()
    response_lines = []

    for product_name, amount_str in items:
        amount = float(amount_str)
        product = await product_repo.get_products_by_names([product_name.lower()])
        
        if len(product) == 1:
            product = product[0]
            calories = product.calories * amount / 100
            proteins = product.proteins * amount / 100
            fats = product.fats * amount / 100
            carbs = product.carbs * amount / 100
            response_lines.append(f"{product_name} ({amount} гр):\n\tКалории: {calories} ккал,\n\tБелки: {proteins} г,\n\tЖиры: {fats} г,\n\tУглеводы: {carbs} г\n\n")
        else:
            response_lines.append(f"Продукт {product_name} не найден.")

    response = "\n".join(response_lines)
    await message.answer(response)