from flask import Blueprint

bp = Blueprint('info', __name__)

from application.info import routes
