from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from application import t, T


class LoginForm(FlaskForm):
    username = StringField(t(T.USER), validators=[DataRequired()])
    password = PasswordField(t(T.PASSWORD), validators=[DataRequired()])
    submit = SubmitField(t(T.SEND))



