from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from application.models import User


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('send')


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    repeat_password = PasswordField('repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('send')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('write a different name.')


class ResetPasswordRequestForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    submit = SubmitField('request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])
    repeat_password = PasswordField('repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('request password reset')
