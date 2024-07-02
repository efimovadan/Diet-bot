import asyncpg

# Удобная прослойка для работы с БД.
# Реализует паттерн Singleton
class Database:
    _instance = None
    _db_conn_dict = None
    _pool = None

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
        cls._pool = await asyncpg.create_pool(
            user=cls._db_conn_dict['user'],
            password=cls._db_conn_dict['password'],
            database=cls._db_conn_dict['database'],
            host=cls._db_conn_dict['host']
        )

    async def execute_query(self, query, params=None, return_type='execute'):
        if self._pool is None:
            raise Exception("Connection pool is not established.")
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                if return_type == 'fetch':
                    return await connection.fetch(query, *params)
                elif return_type == 'fetchval':
                    return await connection.fetchval(query, *params)
                elif return_type == 'fetchrow':
                    return await connection.fetchrow(query, *params)
                else:
                    await connection.execute(query, *params)
                    return True