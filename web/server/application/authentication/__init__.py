from flask import Blueprint

bp = Blueprint('authentication', __name__)

from application.authentication import routes
