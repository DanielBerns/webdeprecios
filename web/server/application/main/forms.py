from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


from application.models import User


class PostForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Send')


class MessageForm(FlaskForm):
    message = TextAreaField('Message', 
                            validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Send')


class EmptyForm(FlaskForm):
    submit = SubmitField('Accept')
