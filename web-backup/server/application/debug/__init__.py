from flask import Blueprint

bp = Blueprint('debug', __name__)

from application.debug import routes
