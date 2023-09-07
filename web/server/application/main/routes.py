from flask import render_template
from flask_login import current_user
from application import db

from application.main import bp

@bp.route('/', methods=['GET'])
def frontpage():
    return render_template('main/frontpage.html')

@bp.route('/index', methods=['GET'])
def index():
    return render_template('main/index.html')

@bp.route('/help', methods=['GET'])
def help():
    return render_template('main/help.html')

