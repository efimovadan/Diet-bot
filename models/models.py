
class User:
    def __init__(self, telegram_id, username, height, weight, age, physical_activity_level, goal, gender):
        self.telegram_id = telegram_id
        self.username = username
        self.height = height
        self.weight = weight
        self.age = age
        self.physical_activity_level = physical_activity_level
        self.goal = goal
        self.gender = gender
        

    def __str__(self):
        return f"User {self.username} with telegram_id {self.telegram_id}"
    
class Product:
    def __init__(self, name: str, proteins: float, fats: float, carbs: float, calories: int):
        self.name = name
        self.proteins = proteins
        self.fats = fats
        self.carbs = carbs
        self.calories = calories