import asyncpg

# Используется для доступа к базе данных
# Реализует паттерн Singleton
class Database:
    _instance = None
    _db_conn_dict = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    @classmethod
    async def initialize(cls, db_conn_dict):
        if cls._db_conn_dict is None:
            cls._db_conn_dict = db_conn_dict
            await cls.connect()

    @classmethod
    async def connect(cls):
        cls.connection = await asyncpg.connect(
            user=cls._db_conn_dict['user'],
            password=cls._db_conn_dict['password'],
            database=cls._db_conn_dict['database'],
            host=cls._db_conn_dict['host']
        )

    async def execute_query(self, query, params=None):
        if not hasattr(self, 'connection'):
            raise Exception("Connection to database is not established.")
        async with self.connection.transaction():
            await self.connection.execute(query, *params)
        