import base64
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for, current_app
from datetime import datetime, timedelta
from application import db, login
from time import time
import json
from PIL import Image
import io
from pathlib import Path 

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    last_message_read_time = db.Column(db.DateTime)
    
    posts = db.relationship('Post', 
                            foreign_keys='Post.user_id',
                            backref='author', 
                            lazy='dynamic')
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    notifications = db.relationship('Notification', 
                                    foreign_keys='Notification.user_id', 
                                    backref='user',
                                    lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username:s}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1024))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post {self.content:s}>'


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Message {self.content:s}>'


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    payload = db.Column(db.Text)
    timestamp = db.Column(db.Float, index=True, default=time)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get_data(self):
        return json.loads(str(self.payload))


STORE_DEPTH = 2
FILES_PER_FOLDER = 256


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Store ({self.id:d})>'
    
    def id2FS(self):
        number = self.id
        digits = [0]*(STORE_DEPTH + 1)
        for i in range(STORE_DEPTH + 1):
            digits[STORE_DEPTH - i] = number % FILES_PER_FOLDER
            number = number // FILES_PER_FOLDER
        parts = [f'{v:>03d}' for v in digits]
        name = ''.join(parts)
        folder = Path(current_app.config['PICTURES'], parts[0], parts[1])
        folder.mkdir(mode=0o700, parents=True, exist_ok=True)
        return folder, name

    @staticmethod
    def create(user):
        store = Store(user_id=user.id)
        db.session.add(store)
        db.session.commit()
        return store


ALLOWED_IMAGES = set(['png', 'jpg', 'jpeg'])


def save_image(image, store):
    try:
        current_app.logger.info('0 save_image start')
        _folder, _name = store.id2FS()
        current_app.logger.info(f'1 save_image {str(_folder):s} {_name:s}')
        image_path = Path(_folder, f'{_name:s}.png')
        current_app.logger.info(f'2 save_image {_name:s} {str(image_path):s}')
        image.save(image_path)
        current_app.logger.info(f'3 save_image {_name:s} image save')                
    except Exception as message:
        current_app.logger.error(f'4 save_image {_name:s} crash: {str(message):s}')        
        abort(500)
