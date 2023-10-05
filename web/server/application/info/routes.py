from flask import render_template
from flask_login import current_user, login_required
from markupsafe import escape

from application import db

from application.info import bp

@bp.route('/<string:category>/<string:city>', methods=['GET'])
def category_city(category, city):
    _category = escape(category)
    _city = escape(city)
    return render_template(f'info/{_category:s}/{_city:s}.html')

# @bp.route('/caleta_olivia', methods=['GET'])
# def caleta_olivia():
#     return render_template('info/cba/caleta_olivia.html')
# 
# @bp.route('/rio_gallegos', methods=['GET'])
# def rio_gallegos():
#     return render_template('info/cba/rio_gallegos.html')
# 
# @bp.route('/comodoro_rivadavia', methods=['GET'])
# def comodoro_rivadavia():
#     return render_template('info/cba/comodoro_rivadavia.html')
# 
# @bp.route('/rada_tilly', methods=['GET'])
# def rada_tilly():
#     return render_template('info/cba/rada_tilly.html')
# 
# @bp.route('/esquel', methods=['GET'])
# def esquel():
#     return render_template('info/cba/esquel.html')
# 
# @bp.route('/puerto_madryn', methods=['GET'])
# def puerto_madryn():
#     return render_template('info/cba/puerto_madryn.html')
# 
# @bp.route('/rawson', methods=['GET'])
# def rawson():
#     return render_template('info/cba/rawson.html')
# 
# @bp.route('/trelew', methods=['GET'])
# def trelew():
#     return render_template('info/cba/trelew.html')

@bp.route('/cba', methods=['GET'])
def cba():
    return render_template('info/cba.html')

@bp.route('/industrias', methods=['GET'])
def industrias():
    return render_template('info/industries.html')

@bp.route('/casas', methods=['GET'])
def casas():
    return render_template('info/houses.html')

@bp.route('/noticias', methods=['GET'])
def noticias():
    return render_template('info/news.html')

@bp.route('/comunidad', methods=['GET'])
def comunidad():
    return render_template('info/community.html')

@bp.route('/sobre_nosotros', methods=['GET'])
def sobre_nosotros():
    return render_template('info/about_us.html')

# Header #4caf50
# Card #3cd400
