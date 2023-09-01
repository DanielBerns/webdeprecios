import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import uuid

from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


from config import Config


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from application.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from application.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from application.main import bp as main_bp
    app.register_blueprint(main_bp)

    from application.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    if not app.debug and not app.testing:
        file_handler = RotatingFileHandler(
            Path(app.config['LOGS_PATH'], 'application.log'), 
            maxBytes=10240, 
            backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.DEBUG)
        app.logger.info('Started')

    return app


from application import models
