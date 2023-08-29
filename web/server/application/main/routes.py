from datetime import datetime
from flask import render_template, current_app
from flask_login import current_user, login_required

from application import db
from application.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET'])
def index():
    return render_template('main/home.html', title='Home')
