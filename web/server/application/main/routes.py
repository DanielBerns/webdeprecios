from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from application import db, t, T

# 202311091936

from application.main import bp
from application.main.forms import PostForm, MessageForm, EmptyForm

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/', methods=['GET'])
def frontpage():
    return render_template('main/frontpage.html')

@bp.route('/index', methods=['GET'])
def index():
    return render_template('main/index.html', title='Indice')

@bp.route('/help', methods=['GET'])
def help():
    return render_template('main/help.html')

# 202311091954

@bp.route('/posts', methods=['GET', 'POST'])
@login_required
def post_create():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(content=form.content.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash(t(T.YOUR_POST_IS_LIVE_NOW))
        return redirect(url_for('main.post_create', page=1))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page, 
        per_page=current_app.config['POSTS_PER_PAGE'], 
        error_out=False)
    
    next_url = url_for('main.post_create', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.post_create', page=posts.prev_num) if posts.has_prev else None
    
    return render_template('post_create.html', 
                           title=t(T.INDEX), 
                           form=form,
                           posts=posts.items, 
                           next_url=next_url,
                           prev_url=prev_url)
