from .db import Database
from models import User

# Реализует паттерн Repository, является Singleton
class UserRepository:
    _instance = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._db = Database()  
            cls._instance = super(UserRepository, cls).__new__(cls)
        return cls._instance

    async def create(self, user: User):
        query = "INSERT INTO users (telegram_id, username, height, weight, age, physical_activity_level, goal, gender) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)"
        params = (user.telegram_id, user.username, user.height, user.weight, user.age, user.physical_activity_level, user.goal, user.gender)
        await self._db.execute_query(query, params)

    async def is_exist(self, telegram_id) -> bool:
        query = "SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id = $1)"
        params = (telegram_id,)
        return  await self._db.execute_query("SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id = $1)", params=(telegram_id,), return_type='fetchval')
    
    async def get_user(self, telegram_id: int) -> User:
        query = "SELECT telegram_id, username, height, weight, age, physical_activity_level, goal, gender FROM users WHERE telegram_id = $1"
        user_data = await self._db.execute_query(query, params=(telegram_id,), return_type='fetchrow')
        if user_data:
            return User(
                telegram_id=user_data['telegram_id'],
                username=user_data['username'],
                height=user_data['height'],
                weight=user_data['weight'],
                age=user_data['age'],
                physical_activity_level=user_data['physical_activity_level'],
                goal=user_data['goal'],
                gender=user_data['gender']
            )
        return None