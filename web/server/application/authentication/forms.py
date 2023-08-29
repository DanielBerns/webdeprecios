from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email, NumberRange, Length
from application.date_validator import DateValidator
from application.models import ALLOWED_IMAGES, User
from application.operations import create_user_with_publisher_rights



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me', default=True)
    submit = SubmitField('Sign In')


class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    accept_tos = BooleanField('I accept the Terms of Service', validators=[DataRequired()])
    submit = SubmitField('Register user')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    
class PublisherForm(FlaskForm):
    firstname = StringField('First name', validators=[DataRequired()])
    lastname = StringField('Last name', validators=[DataRequired()])
    birthdate_year = IntegerField('Birthdate year', validators=[DataRequired()])
    birthdate_month = IntegerField('Birthdate month', validators=[DataRequired()])    
    birthdate_day = IntegerField('Birthdate day', validators=[DataRequired(), DateValidator('birthdate')])
    country = StringField('Country', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    door = StringField('Door', validators=[DataRequired()])
    photo = FileField('Picture', validators=[FileRequired(), FileAllowed(ALLOWED_IMAGES, message='Images Only!')])
    submit = SubmitField('Register Publisher')    
                       
