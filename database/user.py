from .db import Database
from models import User

# Реализует паттерн Repository, является Singleton
class UserRepository:
    _instance = None
    _db = None

    @classmethod
    def initialize(cls):
        if cls._instance is None:
            cls._db = Database()
            cls._instance = cls()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserRepository, cls).__new__(cls)
        return cls._instance

    async def create(self, user: User):
        query = "INSERT INTO users (telegram_id, username, height, weight, age, physical_activity_level) VALUES ($1, $2, $3, $4, $5, $6)"
        params = (user.telegram_id, user.username, user.height, user.weight, user.age, user.physical_activity_level)
        await self._db.execute_query(query, params)
    
    async def is_exist(self, telegram_id):
        query = "SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id = $1)"
        params = (telegram_id,)
        return await self._db.execute_query(query, params)