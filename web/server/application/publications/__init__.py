from flask import Blueprint

bp = Blueprint('publications', __name__)

from application.publications import routes
