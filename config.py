import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ACCESS_KEY = os.environ.get('ACCESS_KEY')
    APPSETTING_ENVIRONMENT = os.environ.get('ENVIRONMENT')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_SERVER = os.environ.get('DB_SERVER')
    DB_URL = os.environ.get('DB_URL')

