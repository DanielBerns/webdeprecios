from datetime import datetime
from pathlib import Path
import jwt # https://pypi.org/project/jwt/
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

from application import db, login
from .mymixins import GetIdMixin # from flask_login import UserMixin


ZERO   = 0
ADMIN  = 1
CREATE = 2
READ   = 4
UPDATE = 8
DELETE = 16


PUBLISHER = CREATE | READ | UPDATE | DELETE


class User(db.Model, GetIdMixin):
    identifier = db.Column(db.Integer, primary_key=True)
    url_suffix = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    rights = db.Column(db.Integer, nullable=False, default=ZERO)
    email = db.Column(db.String(64), unique=True)
    phone = db.Column(db.String(16), unique=True)
    username = db.Column(db.String(32), unique=True)
    verified_email = db.Column(db.Boolean(), default=False)
    verified_phone = db.Column(db.Boolean(), default=False)
    enabled = db.Column(db.Boolean(), default=False)
    enabled_reason = db.Column(db.String(32), default='-')
    
    def __repr__(self):
        return f'<User ({self.identifier:d}:{self.url_suffix})>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def find_password(self, password):
        return check_password_hash(self.password_hash, password)

    def verify(self, mask):
        return (self.rights & mask) == mask

   

@login.user_loader
def load_user(identifier):
    return User.query.get(int(identifier))


class UserAuthInfo(db.Model):
    identifier = db.Column(db.Integer, primary_key=True)
    user_identifier = db.Column(db.Integer, db.ForeignKey('user.identifier'), nullable=False)
    value = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return f'<UserAuthInfo({self.identifier:d}, {self.user_identifier:d}): {self.value:s}>'
    
    @staticmethod
    def find(user):
        return UserAuthInfo.query.filter_by(user_identifier=user.identifier).first()

        
class Admin(db.Model):
    identifier = db.Column(db.Integer, primary_key=True)
    user_identifier = db.Column(db.Integer, db.ForeignKey('user.identifier'), nullable=False)
    
    def __repr__(self):
        return '<Admin({self.identifier:d}, {self.user_identifier:d})>'
    
    @staticmethod
    def find(user):
        return Admin.query.filter_by(user_identifier=user.identifier).first()

    
class Publisher(db.Model):
    identifier = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32), nullable=False)
    lastname = db.Column(db.String(32), nullable=False)
    birthdate = db.Column(db.DateTime(), nullable=False)
    country = db.Column(db.String(32), nullable=False)
    state = db.Column(db.String(32), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    street = db.Column(db.String(32), nullable=False)
    door = db.Column(db.String(64), nullable=False)
    photo = db.Column(db.Integer, db.ForeignKey('store.identifier'), nullable=False)
    user_identifier = db.Column(db.Integer, db.ForeignKey('user.identifier'), nullable=False)
    
    def __repr__(self):
        return f'<Publisher ({self.identifier:d})>'

    def birthdate2str(self):
        return f'{self.birthdate.day:>2d}/{self.birthdate.month:>2d}/{self.birthdate.year:>4d}'

    def address(self):
        return f'{self.country}, {self.state:s}, {self.city:s}, {self.street:s} {self.door:s}'
    
    def photo_url(self):
        return f'{Store.store_url(self.photo):s}.png'
    
    @staticmethod
    def find_by_user(user):
        return Publisher.query.filter_by(user_identifier=user.identifier).first()


FILESYSTEM_DEPTH = 2
FILES_PER_FOLDER = 256


class Store(db.Model):
    identifier = db.Column(db.Integer, primary_key=True)
    url_suffix = db.Column(db.String(32))    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_identifier = db.Column(db.Integer, db.ForeignKey('user.identifier'), nullable=False)

    def __repr__(self):
        return f'<Store ({self.identifier:d})>'
    
    def identifier2FS(self):
        number = self.identifier
        digits = [0]*(FILESYSTEM_DEPTH + 1)
        for i in range(FILESYSTEM_DEPTH + 1):
            digits[FILESYSTEM_DEPTH - i] = number % FILES_PER_FOLDER
            number = number // FILES_PER_FOLDER
        parts = [f'{v:>03d}' for v in digits]
        name = ''.join(parts)
        folder = Path(current_app.config['STORE_PATH'], parts[0], parts[1])
        folder.mkdir(mode=0o700, parents=True, exist_ok=True)
        return folder, name

    def identifier2url(self):
        number = self.identifier
        digits = [0]*(FILESYSTEM_DEPTH + 1)
        for i in range(FILESYSTEM_DEPTH + 1):
            digits[FILESYSTEM_DEPTH - i] = number % FILES_PER_FOLDER
            number = number // FILES_PER_FOLDER
        parts = [f'{v:>03d}' for v in digits]
        name = ''.join(parts)
        return f'{parts[0]:s}/{parts[1]:s}/{name:s}'

    @staticmethod
    def store_url(key):
        store = Store.query.get(key)
        return store.identifier2url()
    
    @staticmethod
    def find_by_user(user):
        return Store.query.filter_by(user_identifier=user.identifier)

    @staticmethod
    def find_by_url_suffix(url_suffix):
        return Store.query.filter_by(url_suffix=url_suffix)


ALLOWED_IMAGES = set(['png', 'jpg', 'jpeg'])


class Post(db.Model):
    identifier = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    url_suffix = db.Column(db.String(32))
    user_identifier = db.Column(db.Integer, db.ForeignKey('user.identifier'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    body = db.Column(db.String(256), nullable=False)
    photo = db.Column(db.Integer, db.ForeignKey('store.identifier'), nullable=False)
    active = db.Column(db.Boolean(), default=False)
    
    def photo_url(self):
        return f'{Store.store_url(self.photo):s}.png'

    @staticmethod
    def find_by_user(user):
        return Post.query.filter_by(user_identifier=user.identifier)

    @staticmethod
    def find_by_url_suffix(url_suffix):
        return Store.query.filter_by(url_suffix=url_suffix)


