import psycopg2

# Используется для доступа к базе данных
# Реализует паттерн Singleton
class Database:
    _instance = None
    _db_url = None  

    @classmethod
    def initialize(cls, db_url):
        if cls._instance is None:
            cls._db_url = db_url
            cls._instance = cls()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connect = psycopg2.connect(dsn=cls._db_url)
            cls._instance.cursor = cls._instance.connect.cursor()
        return cls._instance

    def __del__(self):
        self.cursor.close()
        self.connect.close()

    def create_user(self, user):
        self.cursor.execute(
            "INSERT INTO users (telegram_id, username, height, weight, age, physical_activity_level) VALUES (%s, %s, %s, %s, %s, %s)",
            (user.telegram_id, user.username, user.height, user.weight, user.age, user.physical_activity_level)
        )
        self.connect.commit()