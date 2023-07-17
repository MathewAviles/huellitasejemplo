from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm
from .model import RegistroU

class UserRegisterForm(FlaskForm):
    nombre = StringField('Nombre:' ,[validators.Length(min=4, max=100)])
    username = StringField('Usuario',[validators.Length(min=4, max=100)])
    telefono = StringField('Teléfono:', [validators.DataRequired(), validators.Length(min=10, max=10)]) 
    email= StringField('Correo:', [validators.Email(), validators.DataRequired(), validators.Length(min=10, max=100)])
    password = PasswordField('Contraseña:', [validators.DataRequired(), validators.Length(min=8, max=50), validators.EqualTo('confirm',message='Las contraseñas no coinciden ')])
    confirm= PasswordField('Repita la contraseña: ', [validators.DataRequired(), validators.Length(min=8, max=50)])
    profile = FileField('Foto de perfil', validators=[FileAllowed(['jpg','png','jpeg','gif'], 'Solo imágenes por favor ')])
    submit= SubmitField('RegistroU')
    
    
    def validate_username(self, username):
        if RegistroU.query.filter_by(username=username.data).first():
            raise ValidationError("Este nombre de usuario ya está registrado, ingrese otro")


    def validate_email(self, email):
        if RegistroU.query.filter_by(email=email.data).first():
            raise ValidationError("Este correo ya está registrado, ingrese otro")


class UserLoginForm(FlaskForm):
    email=StringField('Correo: ',[validators.Email(), validators.DataRequired()])
    password=PasswordField('Contraseña: ',[validators.DataRequired()])
    


class ResetPasswordForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired()])
    new_password = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('new_password', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Restablecer Contraseña')
    