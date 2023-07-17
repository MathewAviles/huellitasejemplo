from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    nombre = StringField('Nombre', [validators.Length(min=4, max=25)])
    correo = StringField('Correo', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Contraseña', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='La contraseña no coinside')
    ])
    confirm = PasswordField('Repetir la contraseña')


class LoginForm(Form):
    correo = StringField('Correo', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Contraseña', [validators.DataRequired()])