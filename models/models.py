
class User:
    def __init__(self, telegram_id, username, height, weight, age, physical_activity_level, goal):
        self.telegram_id = telegram_id
        self.username = username
        self.height = height
        self.weight = weight
        self.age = age
        self.physical_activity_level = physical_activity_level
        self.goal = goal
        

    def __str__(self):
        return f"User {self.username} with telegram_id {self.telegram_id}"
    