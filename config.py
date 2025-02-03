import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///buda.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False