import psycopg2

class Database:
    def __init__(self, db_url):
        self.connect = psycopg2.connect(dsn=db_url)
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.cursor.close()
        self.connect.close()

    def create_user(self, user):
        self.cursor.execute(
            "INSERT INTO users (telegram_id, username, height, weight, age, physical_activity_level) VALUES (%s, %s, %s, %s, %s, %s)",
            (user.telegram_id, user.username, user.height, user.weight, user.age, user.physical_activity_level)
        )
        self.connect.commit()
