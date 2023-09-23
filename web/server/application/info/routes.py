from flask import render_template
from flask_login import current_user, login_required

from application import db

from application.info import bp

@bp.route('/comunidad', methods=['GET'])
def community():
    return render_template('info/community.html')

@bp.route('/caleta_olivia', methods=['GET'])
def caleta_olivia():
    return render_template('info/caleta_olivia.html')

@bp.route('/rio_gallegos', methods=['GET'])
def rio_gallegos():
    return render_template('info/rio_gallegos.html')

@bp.route('/comodoro_rivadavia', methods=['GET'])
def comodoro_rivadavia():
    return render_template('info/comodoro_rivadavia.html')

@bp.route('/rada_tilly', methods=['GET'])
def rada_tilly():
    return render_template('info/rada_tilly.html')

@bp.route('/esquel', methods=['GET'])
def esquel():
    return render_template('info/esquel.html')

@bp.route('/puerto_madryn', methods=['GET'])
def puerto_madryn():
    return render_template('info/puerto_madryn.html')

@bp.route('/rawson', methods=['GET'])
def rawson():
    return render_template('info/rawson.html')

@bp.route('/trelew', methods=['GET'])
def trelew():
    return render_template('info/trelew.html')

@bp.route('/cba', methods=['GET'])
def cba():
    return render_template('info/cba.html')

@bp.route('/precios_de_referencia', methods=['GET'])
def precios_de_referencia():
    return render_template('info/precios_de_referencia.html')

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
