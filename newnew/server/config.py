import os
from storage import Storage

APPNAME = 'NewNew'
storage = Storage(APPNAME)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '11235813213455'
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get('DATABASE_URL') or \
        'sqlite:///' + storage.app_db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
