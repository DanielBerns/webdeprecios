import os
from pathlib import Path
from dotenv import load_dotenv

from storage import Storage
from create_storage import BASE

home_path, store_path, logs_path = Storage.start(BASE)
load_dotenv(Path(home_path, 'env'))

class ConfigException(Exception):
    pass

class Config:
    IDENTIFIER = BASE
    HOME_PATH = home_path
    STORE_PATH = store_path
    LOGS_PATH = logs_path
    PICTURES = Storage.container(store_path, 'pictures')
    PRECIOS_CLAROS = Storage.info('precios_claros')    
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1123581235711'
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL') or 'DEBUG'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + str(Path(store_path, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE=10
