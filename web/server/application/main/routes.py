from datetime import datetime
from pathlib import Path

from flask import (
    render_template, 
    flash, 
    redirect, 
    url_for, 
    request, 
    current_app, 
    send_from_directory)
from flask_login import current_user, login_required
from application import db, t, T

from markdown2 import markdown

# 202311091936

from application.main import bp
from application.main.forms import PostForm, MessageForm, EmptyForm
from application.models import User, Post, Message

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
        new_content = markdown(form.content.data)
        new_post = Post(
            content= new_content if new_content else "error",
            author=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        flash(t(T.YOUR_POST_IS_LIVE_NOW))
        return redirect(url_for('main.post_create', page=1))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page, 
        per_page=current_app.config['POSTS_PER_PAGE'], 
        error_out=False
    )
    
    next_url = url_for('main.post_create', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.post_create', page=posts.prev_num) if posts.has_prev else None
    
    return render_template('main/post_create.html', 
                           title=t(T.INDEX), 
                           form=form,
                           posts=posts.items, 
                           next_url=next_url,
                           prev_url=prev_url)


@bp.route('/posts/followed/<username>')
@login_required
def posts_followed(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.followed_posts().paginate(
        page=page, 
        per_page=current_app.config['POSTS_PER_PAGE'], 
        error_out=False)
    
    next_url = url_for('main.posts_followed', 
                       username=username, 
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.posts_followed', 
                       username=username, 
                       page=posts.prev_num) if posts.has_prev else None
    
    return render_template('main/posts_followed.html', 
                           title=t(T.SOME_POSTS),
                           user=user, 
                           posts=posts.items,
                           next_url=next_url, 
                           prev_url=prev_url)

@bp.route('/posts/allofthem')
def posts_allofthem():
   page = request.args.get('page', 1, type=int)
   posts = Post.query.order_by(Post.timestamp.desc()).paginate(
       page=page, 
       per_page=current_app.config['POSTS_PER_PAGE'], 
       error_out=False)
   next_url = url_for('main.posts_allofthem', page=posts.next_num) \
       if posts.has_next else None
   prev_url = url_for('main.posts_allofthem', page=posts.prev_num) \
       if posts.has_prev else None
   return render_template("main/posts_allofthem.html", 
                          title=t(T.ALL_THE_POSTS), 
                          posts=posts.items,
                          next_url=next_url, 
                          prev_url=prev_url)


@bp.route('/message/<recipient>', methods=['GET', 'POST'])
@login_required
def message_create(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        a_message = Message(author=current_user, 
                      recipient=user,
                      content=form.message.data)
        db.session.add(a_message)
        db.session.commit()
        flash(t(T.MESSAGE_SENT))
        return redirect(url_for('main.posts_followed', username=recipient))
    return render_template('main/message_create.html', 
                           title=t(T.SEND_MESSAGE),
                           form=form, 
                           recipient=recipient)

@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page=page, 
            per_page=current_app.config['POSTS_PER_PAGE'], 
            error_out=False)
    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('main/messages.html', 
                           title=t(T.MESSAGES),
                           nav_h1=t(T.MESSAGES_LIST),
                           messages=messages.items,
                           next_url=next_url, 
                           prev_url=prev_url)


@bp.route('/user/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(t(USER_NOT_FOUND) + f' {username:s}')
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(t(EACH_USER_FOLLOWS_HER_POSTS))
            return redirect(url_for('main.user_contact', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(t(T.NOW_YOU_ARE_FOLLOWING_THE_POSTS_BY) + username)
        return redirect(url_for('main.user_contact', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/user/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(t(T.USER_NOT_FOUND) + username)
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(t(T.EACH_USER_FOLLOWS_HER_POSTS))
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(t(T.YOU_HAVE_STOPPED_FOLLOWING_THE_POST_BY) + username)
        return redirect(url_for('main.user_contact', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/user/contact/<username>')
@login_required
def user_contact(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('main/user_contact.html', 
                           user=user, 
                           form=form)

@bp.route('/precios_claros/news', methods=['GET'])
def news_index():
    directory = Path(
        current_app.config['PRECIOS_CLAROS'],
    )
    if directory.exists():
        return send_from_directory(directory, 'news.html')
    else:
        flash(f'Error: news - {str(directory):s}')
        return redirect(url_for('main.index'))


@bp.route('/precios_claros/index/<timestamp>/<place>', methods=['GET'])
def precios_claros_index(timestamp, place):
    directory = Path(
        current_app.config['PRECIOS_CLAROS'],
        timestamp,
        place
    )
    if directory.exists():
        return send_from_directory(directory, 'index.html')
    else:
        flash(f'Error: {timestamp:s}/{place:s} - {str(directory):s}')
        return redirect(url_for('main.index'))
        
@bp.route('/precios_claros/category/<timestamp>/<place>/<folder>/<name>', methods=['GET'])
def precios_claros_category(timestamp, place, folder, name):
    directory = Path(
        current_app.config['PRECIOS_CLAROS'],
        timestamp,
        place,
        folder
    )
    if directory.exists():
        return send_from_directory(directory, f'{name:s}.html')
    else:
        flash('Error: {timestamp:s}/{place:s}/{folder:s}/{name:s}')
        return redirect(url_for('main.index'))

