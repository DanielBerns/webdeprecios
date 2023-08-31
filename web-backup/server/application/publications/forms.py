from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import ValidationError, DataRequired, NumberRange, Length

from application.operations import ALLOWED_IMAGES


class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=32, max=256)])
    active = BooleanField('Active')
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(ALLOWED_IMAGES, message='Images Only!')])
    submit = SubmitField('Submit')

