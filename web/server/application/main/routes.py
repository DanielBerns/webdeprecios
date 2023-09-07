from datetime import datetime
from pathlib import Path
import os
import uuid

from flask import render_template, flash, redirect, url_for, request, current_app, jsonify, send_from_directory
from flask_login import current_user, login_required

from application import db
from application.main.forms import PostForm, EditProfileForm, MessageForm, EmptyForm


from application.main import bp
from application.models import User, Post, Message, Notification, Store


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
    return render_template('main/index.html')

@bp.route('/info', methods=['GET'])
def info():
    return render_template('main/info.html', title='info')

@bp.route('/help', methods=['GET'])
def help():
    return render_template('main/help.html', title='help')

@bp.route('/chakana', methods=['GET'])
def chakana():
    return render_template('main/chakana.html', title='chakana')

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.followed_posts().paginate(
        page, 
        current_app.config['POSTS_PER_PAGE'], 
        False)
    next_url = None
    if posts.has_next:
        next_url = url_for('main.user', 
                           username=user.username, 
                           page=posts.next_num)
    prev_url = None
    if posts.has_prev:
        prev_url = url_for('main.user', 
                           username=user.username, 
                           page=posts.prev_num)
    form = EmptyForm()
    return render_template('user.html', 
                           user=user, 
                           posts=posts.items,
                           next_url=next_url, 
                           prev_url=prev_url,
                           form=form)


@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user_popup.html', 
                           user=user, 
                           form=form)





@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username:s} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username:s}!')
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'User {username:s} not found.')
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username:s}.')
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/explore')
@login_required
def explore():
   page = request.args.get('page', 1, type=int)
   posts = Post.query.order_by(Post.timestamp.desc()).paginate(
       page, current_app.config['POSTS_PER_PAGE'], False)
   next_url = url_for('main.explore', page=posts.next_num) \
       if posts.has_next else None
   prev_url = url_for('main.explore', page=posts.prev_num) \
       if posts.has_prev else None
   return render_template("index.html", 
                          title='Explore', 
                          posts=posts.items,
                          next_url=next_url, 
                          prev_url=prev_url)


@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        a_message = Message(author=current_user, 
                      recipient=user,
                      content=form.message.data)
        db.session.add(a_message)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', 
                           title='Send Message',
                           form=form, 
                           recipient=recipient)

@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, 
            current_app.config['POSTS_PER_PAGE'], 
            False)
    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', 
                           messages=messages.items,
                           next_url=next_url, 
                           prev_url=prev_url)

@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])


@bp.route('/pictures/<string:requested_resource_uuid>')
@login_required
def get_picture(requested_resource_uuid):
    current_app.logger.info(f'get_pictures.1 {requested_resource_uuid:s}')    
    resource = Experiment.query.filter_by(resource_uuid=requested_resource_uuid).first_or_404()
    current_app.logger.info('get_pictures.2')    
    store = Store.query.filter_by(id=resource.store_id).first_or_404()
    current_app.logger.info('get_pictures.3')        
    image_path, filename = store.id2FS()
    current_app.logger.info(f'get_pictures.4 {str(image_path):s} {filename:s}')        
    return send_from_directory(image_path, filename+'.png')
