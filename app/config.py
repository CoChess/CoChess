import os

class Config:
    SECRET_KEY = "your_secret_key_here"
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

