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
