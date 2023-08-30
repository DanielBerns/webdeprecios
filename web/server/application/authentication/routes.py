import uuid
import io
import datetime
from pathlib import Path


from PIL import Image
from werkzeug.urls import url_parse
from flask import render_template, redirect, url_for, flash, request, abort, current_app


from flask_login import login_user, logout_user, current_user, login_required
from application.authentication import bp
from application.authentication.forms import LoginForm, UserForm, PublisherForm
from application.models import User, Publisher, Admin, ZERO, ADMIN, CREATE, READ, UPDATE, DELETE
from application.operations import (
    create_user, 
    enable_user, 
    create_date, 
    underage, 
    create_photo, 
    create_publisher, 
    get_user_by_url_suffix,
    get_user_and_producer_by_url_suffix)


def get_next_page():
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('main.index')
    return next_page


def process_user_form(form):
    data = form.data
    email = data['email']
    phone = data['phone']
    username = data['username']
    password = data['password']
    repeat_password = data['repeat_password']    
    accept_tos = data['accept_tos']
    if accept_tos:
        user, user_auth_info = create_user(
            email, phone, username, password, 
            (CREATE | READ | UPDATE | DELETE))
        return user, user_auth_info
    else:
        flash('You have not accepted the terms of service!')
        flash('No user account for you!')
        return None, None


@bp.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = UserForm()
    if form.validate_on_submit():
        user, user_auth_info = process_user_form(form)
        if user and user_auth_info:
            flash('You are a registered user!')
            return redirect(url_for('authentication.register_publisher', 
                                    user_url_suffix=user.url_suffix))
        else:
            return redirect(url_for('debug.show', state='authentication.register_user'))
    return render_template('authentication/register_user.html', form=form)


@bp.route('/goodbye', methods=['GET'])
def goodbye():
    return render_template('authentication/goodbye.html')


def process_publisher_form(form, user):
    publisher = None
    data = form.data
    firstname = data['firstname']
    lastname = data['lastname']
    birthdate_year = data['birthdate_year']
    birthdate_month = data['birthdate_month']
    birthdate_day = data['birthdate_day']
    country = data['country']
    state = data['state']
    city = data['city']
    street = data['street']
    door = data['door']
    image = data['photo']
    enabled = True
    enabled_reason = 'No processed data yet!'
    try:
        birthdate = create_date(birthdate_year, birthdate_month, birthdate_day)
        if birthdate:
            if underage(birthdate):
                message = 'You are too young!'
                flash(message)
                current_app.logger.error(f'process_publisher_form: {message:s} - {str(year):s}/{str(month):s}/{str(day):s}')                
                enabled = False
                enabled_reason = message
        else:    
            message = 'No valid birthdate!'
            flash(message)
            current_app.logger.error(f'process_publisher_form: {message:s} - {str(year):s}/{str(month):s}/{str(day):s}')
            birthdate = get_today()
            enabled = False
            enabled_reason = message
        photo = create_photo(
            image, 
            user)
        publisher = create_publisher(
            firstname,
            lastname,
            birthdate,
            country,
            state,
            city,
            street,
            door,
            photo,
            user)
        if publisher:
            message = "Publisher info saved succesfully!"
            flash(message)
            current_app.logger.info(f'process_publisher_form: {message:s} - {repr(publisher):s}')
            enabled_reason = message
        else:
            message = "We can not save your info. Please edit and try again!"
            flash(message)
            current_app.logger.error(f'process_publisher_form: {message:s}')            
    except Exception as error:
        message = "We can not save your info. Please edit and try again!"
        flash(message)
        current_app.logger.error(f'process_publisher_form: {message:s} - {str(error):s}')
    else:
        try:
            enable_user(user, enabled, enabled_reason)
        except Exception as error:
            message = "Unexpected error!"
            flash(message)
            current_app.logger.error(f'process_publisher_form: {message:s} - {str(error):s}')
            abort(500)
    return publisher


@bp.route('/register_publisher/<string:user_url_suffix>', methods=['GET', 'POST'])
def register_publisher(user_url_suffix):
    user = get_user_by_url_suffix(user_url_suffix)
    if user:
        if current_user.is_authenticated:
            next_page = get_next_page()
            return redirect(next_page)
        form = PublisherForm()
        if form.validate_on_submit():
            publisher = process_publisher_form(form, user)
            if publisher:    
                login_user(user, remember=True)
                flash('You are a registered publisher!')
                return redirect(url_for('authentication.review', user_url_suffix=user.url_suffix))
            else:
                return redirect(url_for('debug.show', state='authentication.register_publisher'))
        return render_template('authentication/register_publisher.html', 
                               form=form, 
                               user=user,
                               html_title='authentication-register_publisher',
                               website=current_app.config['WEBSITE'])
    else:
        abort(404)


def process_login_form(form):
    message = 'no process_login_form yet!'
    flash(message)
    current_app.logger.error(message)
    return False


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        next_page = get_next_page()
        return redirect(next_page)
    form = LoginForm()
    if form.validate_on_submit():
        user, remember_me = process_login_form(form)
        if user:
            login_user(user, remember=True)
            flash('Succesful login!')
            return redirect(next_page)
        else:
            return redirect(url_for('debug.show', state='authentication.login'))
    return render_template('authentication/login.html', 
                           form=form, 
                           html_title='authentication-login',
                           website=current_app.config['WEBSITE'])


@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('main.index'))


@bp.route('/review/<string:user_url_suffix>', methods=['GET'])
@login_required
def review(user_url_suffix):
    user, publisher = get_user_and_producer_by_url_suffix(user_url_suffix)
    if user and publisher:
        if user == current_user:
            return render_template('authentication/review.html', 
                                    publisher=publisher, 
                                    user=user, 
                                    html_title='authentication-review',
                                    website=current_app.config['WEBSITE'])  
    abort(404)


@bp.route('/show_users/<string:url_suffix>', methods=['GET'])
@login_required
def show_users(url_suffix):
    if current_user.url_suffix == url_suffix:
        if current_user.verify(ADMIN):
            all_the_users = User.query.order_by(User.identifier)            
            return render_template(
                'authentication/show_users.html', 
                users=all_the_users, 
                html_title='authentication-show_users',
                website=current_app.config['WEBSITE'])
    abort(404)


@bp.route('/show_publishers/<string:url_suffix>', methods=['GET'])
@login_required
def show_publishers(url_suffix):
    if current_user.url_suffix == url_suffix:
        if current_user.verify(ADMIN):
            all_the_publishers = Publisher.query.order_by(Publisher.identifier)            
            return render_template(
                'authentication/show_publishers.html', 
                publishers=all_the_publishers, 
                html_title='authentication-show_publishers',
                website=current_app.config['WEBSITE'])
    abort(404)
