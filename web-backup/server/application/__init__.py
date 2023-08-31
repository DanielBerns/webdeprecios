import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from application.api import FirebaseAPI as AuthenticationAPI

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'authentication.login'
login.login_message = 'Please sign in to access this page.'
authentication_api = AuthenticationAPI()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from application.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    from application.debug import bp as debug_bp
    app.register_blueprint(debug_bp, url_prefix='/debug')
    
    from application.authentication import bp as authentication_bp
    app.register_blueprint(authentication_bp, url_prefix='/authentication')

    from application.publications import bp as publications_bp
    app.register_blueprint(publications_bp, url_prefix='/publications')
    
    from application.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    if not app.testing:
        log_path = Path(app.config['DOT_PATH'], 'logs')
        log_path.mkdir(mode=0o700, parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(Path(log_path, 'application.log'), maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        logging_level = logging.DEBUG
        file_handler.setLevel(logging_level)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging_level)
        app.logger.info('Started')

    return app

from application import models
