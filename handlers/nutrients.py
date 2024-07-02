from aiogram import Dispatcher
from aiogram.filters.command import Command
from .message_text import message_dict
from aiogram import types
from database import UserRepository
from nutrients import calculate_nutrients

import csv
import re

def register_nutrients_handlers(dp: Dispatcher):
    dp.message.register(cmd_daily, Command(commands="daily"))
    dp.message.register(cmd_product, Command(commands="product"))


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
    product_name = message.text.lower()  # Получаем текст сообщения и приводим к нижнему регистру
    product_name_pattern = re.compile(rf"\b{product_name}(ы|а|ов|и)?\b", re.IGNORECASE)  # Создаём шаблон поиска
    
    parts = message.text.split()
    
    # Проверяем, есть ли после команды текст
    if len(parts) > 1:
        products_names = [part.lower() for part in parts[1:]]
    else:
        product_name = ""  # Если текст после команды отсутствует, используем пустую строку

    matched_products = []  

    # Читаем данные из файла
    with open('nutrients/products.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            for product_name in products_names:
                # Проверяем, соответствует ли название продукта шаблону поиска
                if row['Продукты'].lower() == product_name or product_name_pattern.search(row['Продукты'].lower()):
                    matched_products.append(row)

    if matched_products:
        response = "Найденные продукты:\n\n" + "\n\n".join([
            f"{product['Продукты']}: \n\t\t{product['Ккал']} Ккал."
            f"\n\t\tБелки: {product['Белки']} г.\n\t\tЖиры: {product['Жиры']} г.\n\t\tУглеводы: {product['Углеводы']} г."
            for product in matched_products
        ])
    else:
        response = "Продукты не найдены."

    await message.reply(response)  
