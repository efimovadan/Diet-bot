import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.config = {
            'token': os.getenv('TOKEN'),
            'bot_name': os.getenv('BOT_NAME'),
            'db_url': os.getenv('DATABASE_URL'),
        }
    # Задаём поведение конфига при обращении к его элементам по ключу
    # То есть мы можем обращаться к конфигу как к словарю
    def __getitem__(self, key):
        return self.config.get(key)

    def __setitem__(self, key, value):
        self.config[key] = value

    def __delitem__(self, key):
        del self.config[key]