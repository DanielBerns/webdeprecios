from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length
from wtforms.validators import InputRequired

from application.models import User


class PostForm(FlaskForm):
    content = TextAreaField('Escriba', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Publique')


class EditProfileForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    about_me = TextAreaField('Sobre mi', validators=[Length(min=0, max=140)])
    submit = SubmitField('Publique')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Escriba un nombre de usuario diferente.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Aceptar')


class MessageForm(FlaskForm):
    message = TextAreaField('Mensaje', 
                            validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Enviar')


class NetlistForm(FlaskForm):
    left_1 = RadioField('left_1', choices = [('N0','N0'),('N1','N1'), ('N2','N2'),('N3','N3'), ('N4','N4')])
    left_2 = RadioField('left_2', choices = [('N0','N0'),('N1','N1'), ('N2','N2'),('N3','N3'), ('N4','N4')])
    left_3 = RadioField('left_3', choices = [('N0','N0'),('N1','N1'), ('N2','N2'),('N3','N3'), ('N4','N4')])
    left_4 = RadioField('left_4', choices = [('N0','N0'),('N1','N1'), ('N2','N2'),('N3','N3'), ('N4','N4')])
    
    right_1 = RadioField('right_1', choices = [('N0','N0'),('N1','N1'), ('N2','N2'),('N3','N3'), ('N4','N4')])
    right_2 = RadioField('right_2', choices = [('N0','N0'),('N1','N1'), ('N2','N2'),('N3','N3'), ('N4','N4')])
    right_3 = RadioField('right_3', choices = [('N0','N0'),('N1','N1'), ('N2','N2'),('N3','N3'), ('N4','N4')])
    right_4 = RadioField('right_4', choices = [('N0','N0'),('N1','N1'), ('N2','N2'),('N3','N3'), ('N4','N4')])
    submit = SubmitField('Submit')    
