from flask import render_template
from flask_login import current_user, login_required

from application import db

from application.info import bp

@bp.route('/comunidad', methods=['GET'])
def community():
    return render_template('info/community.html')

@bp.route('/caleta_olivia', methods=['GET'])
def city_caleta_olivia():
    return render_template('info/city.html')

@bp.route('/comodoro_rivadavia', methods=['GET'])
def city_comodoro_rivadavia():
    return render_template('info/city.html')

@bp.route('/esquel', methods=['GET'])
def city_esquel():
    return render_template('info/city.html')

@bp.route('/puerto_madryn', methods=['GET'])
def city_esquel():
    return render_template('info/city.html')

@bp.route('/rawson', methods=['GET'])
def city_rawson():
    return render_template('info/city.html')

@bp.route('/trelew', methods=['GET'])
def cityesquel():
    return render_template('info/city.html')

@bp.route('/cba', methods=['GET'])
def cba():
    return render_template('info/cba.html')

@bp.route('/precios_de_referencia', methods=['GET'])
def cba():
    return render_template('info/precios_de_referencia.html')

@bp.route('/industrias', methods=['GET'])
def industries_stats():
    return render_template('info/industries.html')

@bp.route('/casas', methods=['GET'])
def houses_stats():
    return render_template('info/houses.html')

@bp.route('/sobre_nosotros', methods=['GET'])
def about_us():
    return render_template('info/about_us.html')

