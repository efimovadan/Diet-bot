import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        db_url = os.getenv('DATABASE_URL')
        db_params = dict(param.split('=') for param in db_url.split())
        self.config = {
            'token': os.getenv('TOKEN'),
            'bot_name': os.getenv('BOT_NAME'),
            'db': {
                'user': db_params.get('user'),
                'password': db_params.get('password'),
                'database': db_params.get('dbname'),
                'host': db_params.get('host'),
            }
        }
    # Задаём поведение конфига при обращении к его элементам по ключу при помощи всяких "магических" методов
    # То есть мы можем обращаться к конфигу как к словарю
    def __getitem__(self, key):
        return self.config.get(key)

    def __setitem__(self, key, value):
        self.config[key] = value

    def __delitem__(self, key):
        del self.config[key]