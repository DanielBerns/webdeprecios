from flask import render_template, request, url_for, current_app
from flask_login import current_user, login_required
from markupsafe import escape

from application import db
from application.models import User
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

@bp.route('/observatorio', methods=['GET'])
def observatorio():
    username = "observatorio"
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.followed_posts().paginate(
        page=page, 
        per_page=current_app.config['POSTS_PER_PAGE'], 
        error_out=False)
    next_url = url_for('info.observatorio', 
                       username=username, 
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('info.observatorio', 
                       username=username, 
                       page=posts.prev_num) if posts.has_prev else None

    return render_template('info/observatorio.html', 
                           user=user, 
                           posts=posts.items,
                           next_url=next_url, 
                           prev_url=prev_url)


@bp.route('/sobre_nosotros', methods=['GET'])
def sobre_nosotros():
    return render_template('info/about_us.html')

# Header #4caf50
# Card #3cd400
