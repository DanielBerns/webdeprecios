import datetime
import io
from pathlib import Path

from werkzeug.urls import url_parse
from flask import render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_user, logout_user, current_user, login_required

from application.publications import bp
from application.publications.forms import CreatePostForm
from application.operations import get_user_by_url_suffix, create_post, create_photo, get_post_by_url_suffix, get_posts


def process_create_post_form(user, form):
    current_app.logger.info('process_create_post_form: start')
    post = None
    try:
        data = form.data
        title = data['title']
        body = data['body']
        image = data['photo']  
        active = data['active']
        photo = create_photo(image, user)
        post = create_post(user, title, body, photo.identifier, active)
    except Exception as error:
        current_app.logger.error(f'process_create_post_form: failure {str(error):s}')
    else:
        current_app.logger.info(f'process_create_post_form: success {post.url_suffix:s}')
    return post

@bp.route('/create/<string:user_url_suffix>', methods=['GET', 'POST'])
@login_required
def create(user_url_suffix):
    user = get_user_by_url_suffix(user_url_suffix)
    if user == current_user:
        form = CreatePostForm()
        if form.validate_on_submit():
            post = process_create_post_form(user, form)
            if post:
                flash("You have created a new post! Let's review it.")
                return redirect(
                    url_for('publications.review', 
                            user_url_suffix=user_url_suffix, 
                            post_url_suffix=post.url_suffix))
            else:
                message = f"Unexpected error at publications.create"
                flash(message)
                abort(500)
        return render_template('publications/create.html', form=form)
    else:
        abort(404)


@bp.route('/review/<string:user_url_suffix>/<string:post_url_suffix>', methods=['GET'])
@login_required
def review(user_url_suffix, post_url_suffix):
    user = get_user_by_url_suffix(user_url_suffix)
    post = get_post_by_url_suffix(post_url_suffix)
    if user and post:
        return render_template('publications/review.html', 
                               post=post, 
                               user=current_user)
    else:
        abort(404)


@bp.route('/user_timeline/<string:user_url_suffix>/<int:page>', methods=['GET'])
@login_required
def user_timeline(user_url_suffix, page):
    if user_url_suffix == current_user.url_suffix:
        page = request.args.get('page', 1, type=int)
        posts = get_posts(current_user, page)
        items = posts.items
        if items:
            next_url = url_for('publications.user_timeline', user_url_suffix=user_url_suffix, page=posts.next_num) if posts.has_next else None
            previous_url = url_for('publications.user_timeline', user_url_suffix=user_url_suffix, page=posts.prev_num) if posts.has_prev else None
            get_a_post = lambda k: items[k] if len(items) > k else None
            return render_template(
                'publications/user_timeline.html', 
                post_0=get_a_post(0), post_1=get_a_post(1), post_2=get_a_post(2), post_3=get_a_post(3),
                next_url=next_url, 
                previous_url=previous_url,
                user=current_user) 
    else:
        abort(404)
