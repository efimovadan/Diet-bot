from models import User
from database import ProductRepository
import numpy as np
from scipy.optimize import linprog

def calculate_nutrients(user: User):
    activity_factors = [1.2, 1.375, 1.55]
    
    goal_factors = [0.85, 1.0, 1.15]

    
    if user.gender:  # Мужчина
        bmr = 88.362 + (13.397 * user.weight) + (4.799 * user.height) - (5.677 * user.age)
    else:  
        bmr = 447.593 + (9.247 * user.weight) + (3.098 * user.height) - (4.330 * user.age)

    daily_calories = bmr * activity_factors[user.physical_activity_level] * goal_factors[user.goal]

    
    proteins = daily_calories * 0.3 / 4  # 30% от калорий / 4, т.к 1 г белка = 4 ккал
    fats = daily_calories * 0.25 / 9  # 25% от калорий / 9, т.к 1 г жира = 9 ккал
    carbs = daily_calories * 0.45 / 4  # 45% от калорий / 4, т.к 1 г углеводов = 4 ккал

    return {
        "calories": round(daily_calories),
        "proteins": round(proteins),
        "fats": round(fats),
        "carbs": round(carbs)
    }

# Для того чтобы набрать диету решим задачу линейного программирования в функции solve_diet
# Там классическая задача оптимизации с ограничениями на положительность ответа(нельзя взять отрицательное количество продукта)
# Ещё я добавила штраф за неиспользование продукта, чтобы диета была чуть
async def calculate_daily_diet(user: User, product_names=[]) -> list:
    product_repo = ProductRepository()
    daily_nutrients = calculate_nutrients(user)
    
    proteins = daily_nutrients['proteins']
    fats = daily_nutrients['fats']
    carbs = daily_nutrients['carbs']

    if product_names == []:
        products = await product_repo.get_products()
    else:
        products = await product_repo.get_products_by_names(product_names)
    
    return solve_diet(products, proteins, fats, carbs)



def solve_diet(products, proteins, fats, carbs, diversity_importance=1.5):
    non_usage_penalty = 1e-6
    c = np.array([non_usage_penalty + diversity_importance for _ in products])
    
    A_eq = np.array([[product.proteins, product.fats, product.carbs] for product in products]).T / 100
    b_eq = np.array([proteins, fats, carbs])
    bounds = [(0, None) for _ in products]

    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    if result.success:
        grams = result.x        
        return [(product.name, round(gram, 2)) for product, gram in zip(products, grams) if gram > 0]
    else:
        return []