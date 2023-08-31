from pathlib import Path
import io
import uuid

from PIL import Image

from application import login, db, authentication_api
from application.models import User, UserAuthInfo, Publisher, Admin, Store, Post, ZERO, ADMIN, CREATE, READ, UPDATE, DELETE
from flask import flash, current_app

from datetime import datetime, date, timedelta


@login.user_loader
def load_user(identifier):
    return User.query.get(int(identifier))


def create_url_suffix():
    return uuid.uuid4().hex


def get_user_by_url_suffix(user_url_suffix):
    return User.query.filter_by(url_suffix=user_url_suffix).first()


def get_user_and_producer_by_url_suffix(user_url_suffix):
    user = User.query.filter_by(url_suffix=user_url_suffix).first()
    if user:
        publisher = Publisher.query.filter_by(user_identifier=user.identifier).first()
        return user, publisher
    else:
        return None, None


ALLOWED_IMAGES = set(['png', 'jpg', 'jpeg'])


def create_store(user):
    store = None
    current_app.logger.info('create_store:0')
    try:
        store = Store(user_identifier=user.identifier)
        db.session.add(store)
        db.session.commit()
    except Exception as message:
        current_app.logger.error('create_store:1 - no store')
    return store


def create_photo(image_file, user):
    store = None
    try:
        current_app.logger.info('create_photo:0 start')
        store = create_store(user)
        current_app.logger.info(f'create_photo:1 created store {store.identifier:d}')
        folder, name = store.identifier2FS()
        current_app.logger.info(f'create_photo:2 {str(folder):s} {name:s}')
        image_path = Path(folder, f'{name:s}.png')
        current_app.logger.info(f'create_photo:3 {name:s} {str(image_path):s}')
        image_bytes = io.BytesIO(image_file.read())
        current_app.logger.info(f'create_photo:4 {name:s} image_file')
        photo = Image.open(image_bytes)
        current_app.logger.info(f'create_photo:5 {name:s} image open')        
        photo.save(image_path, 'png')
        current_app.logger.info(f'create_photo:6 {name:s} image save')
    except Exception as error:
        message = "No photo!"
        current_app.logger.error(f'create_photo:7 {str(error):s}')        
    return store


def register_user_with_email_and_password(email, password):
    auth_info = None
    try:
        api_response = authentication_api.sign_up_with_email_and_password(email, password)
    except Exception as message:
        flash(f'Creation of an user account with email {email:s} fails! (1)')
        current_app.logger.error(f'register_user_with_email_and_password:1 - {email:s} - no api_response')        
    else:
        try:
            errors = api_response['errors']
            flash(f'Creation of an user account with email {email:s} fails! (2)')
            current_app.logger.error(f'register_user_with_email_and_password:2 - {email:s} - {str(api_response):s}')
        except KeyError:
            try:
                # idToken = api_response['idToken']
                # expiresIn = api_response['expiresIn']
                email = api_response['email']
                refreshToken = api_response['refreshToken']
                localId = api_response['localId']
                auth_info = (refreshToken, localId)
            except KeyError as message:
                flash(f'User account creation fails! (3)')
                current_app.logger.error(f'register_user_with_email_and_password:3 - {email:s} - {str(api_response):s}')
    return auth_info


def create_user(email, phone, username, password, rights):
    user = None
    user_auth_info = None
    auth_info = register_user_with_email_and_password(email, password)
    if auth_info:
        try:
            user = User(url_suffix=create_url_suffix(),
                        email=email, 
                        phone=phone,
                        username=username,
                        rights=rights
                        )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
        except Exception as error:
            message = 'create_user:1 failure!'
            flash(message)
            current_app.logger.error(f'{message:s} - {str(error):s}')
        else:
            try:
                user_auth_info = UserAuthInfo(
                    user_identifier=user.identifier,
                    value=str(auth_info)      
                    )
                db.session.add(user_auth_info)
                db.session.commit()            
            except Exception as error:
                message = 'create_user:2 failure!'
                flash(message)
                current_app.logger.error(f'{message:s} - {str(error):s}')
    if user and user_auth_info:
        current_app.logger.info(f'create_user:3 - success')
        current_app.logger.info(f'create_user:3 {repr(user):s}')
        current_app.logger.info(f'create_user:3 {repr(user_auth_info):s}')
        flash('User account created successfully!')
        return user, user_auth_info
    if user:
        current_app.logger.error(f'create_user:4 - {repr(user):s}')
    else:
        current_app.logger.error(f'create_user:5 - no user')
    if user_auth_info:
        current_app.logger.error(f'create_user:6 - {repr(user_auth_info):s}')  
    else:
        current_app.logger.error(f'create_user:7 - no user_auth_info')
    flash('We have a problem with your data! Please, try again later!')
    return None, None

                    
def create_user_with_publisher_rights(email, phone, username, password):
    """create user
    """
    user, user_auth_info = create_user(
        email, 
        phone, 
        username,
        password, 
        (CREATE | READ | UPDATE | DELETE))
    return user, user_auth_info

                    
def create_user_with_admin_rights(email, phone, username, password):
    user, error_feedback = create_user(
        email, 
        phone, 
        username,
        password, 
        (ADMIN | CREATE | READ | UPDATE | DELETE))
    return user


def authenticate_user(email, password):
    result = authentication_api.sign_in_with_email_and_password(email, password)    
    if result:
        return User.query.filter_by(email=email).first()
    else:
        return None


def enable_user(user, enabled, enabled_reason):
    user.enabled = enabled
    user.enabled_reason = enabled_reason
    db.session.commit()

    
def create_date(year, month, day):
    try:
        return date(year, month, day)
    except ValueError:
        return None

    
def get_today():
    return date.today()
    

def underage(birthdate):
    return (date.today() - birthdate) < timedelta(days=18*365+5)


def create_publisher(
            firstname,
            lastname,
            birthdate,
            country,
            state,
            city,
            street,
            door,
            photo,
            user
            ):
    publisher = Publisher(
        firstname=firstname,
        lastname=lastname,
        birthdate=birthdate,
        country=country,
        state=state,
        city=city,
        street=street,
        door=door,
        photo=photo.identifier,
        user_identifier=user.identifier)
    db.session.add(publisher)
    db.session.commit()
    return publisher


def create_post(
        user, 
        title, 
        body, 
        photo, 
        active
        ):
    post = Post(url_suffix=create_url_suffix(),
                user_identifier=user.identifier, 
                title=title,
                body=body,
                photo=photo,
                active=active)
    db.session.add(post)
    db.session.commit()
    return post


def get_post_by_url_suffix(post_url_suffix):
    return Post.query.filter_by(url_suffix=post_url_suffix).first()


POSTS_PER_PAGE = 4


def get_posts(user, page):
    return Post.query.filter_by(user_identifier=user.identifier).order_by(
        Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
