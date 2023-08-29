import os
from pathlib import Path
from dotenv import load_dotenv


dot_path = Path('~', '.server').expanduser()
store_path = Path(dot_path, 'store')
load_dotenv(str(Path(dot_path, 'env')))


class Config(object):
    BASE_PATH = Path(__file__).parent
    WEBSITE = os.environ.get('WEBSITE') or 'website'
    DOT_PATH = dot_path
    STORE_PATH = store_path
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL') or "DEBUG"
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1123581235711'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + str(Path(dot_path, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
