from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length
from wtforms.validators import InputRequired

from application.models import User


class PostForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Send')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Send')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Write a different username')


class EmptyForm(FlaskForm):
    submit = SubmitField('Accept')


class MessageForm(FlaskForm):
    message = TextAreaField('Message', 
                            validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Send')

