from models import User

def calculate_nutrients(user: User):
    activity_factors = [1.2, 1.375, 1.55]
    
    goal_factors = [0.85, 1.0, 1.15]

    
    if user.gender:  # Мужчина
        bmr = 88.362 + (13.397 * user.weight) + (4.799 * user.height) - (5.677 * user.age)
    else:  
        bmr = 447.593 + (9.247 * user.weight) + (3.098 * user.height) - (4.330 * user.age)

    daily_calories = bmr * activity_factors[user.physical_activity_level] * goal_factors[user.goal]

    
    proteins = daily_calories * 0.3 / 4  # 30% от калорий и делим на 4, так как 1 г белка = 4 ккал
    fats = daily_calories * 0.25 / 9  # 25% от калорий и делим на 9, так как 1 г жира = 9 ккал
    carbs = daily_calories * 0.45 / 4  # 45% от калорий и делим на 4, так как 1 г углеводов = 4 ккал

    return {
        "calories": round(daily_calories),
        "proteins": round(proteins),
        "fats": round(fats),
        "carbs": round(carbs)
    }