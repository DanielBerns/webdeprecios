from flask import render_template
from flask_login import current_user, login_required

from application import db

from application.info import bp

@bp.route('/cba', methods=['GET'])
def cba():
    return render_template('info/cba.html')

@bp.route('/nlp', methods=['GET'])
def index():
    return render_template('info/nlp.html')

@bp.route('/price_ranges', methods=['GET'])
def info():
    return render_template('info/price_ranges.html')

@bp.route('/oil_stats', methods=['GET'])
def info():
    return render_template('info/oil_stats.html')

@bp.route('/about_us', methods=['GET'])
def info():
    return render_template('info/about_us.html')
