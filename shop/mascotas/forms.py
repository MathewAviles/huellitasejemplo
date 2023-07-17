from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, SelectField, DateField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired



class Addmascotas(Form): 
    nombre = StringField('Nombre', [validators.DataRequired()])
    edad = IntegerField('Edad', [validators.DataRequired()])    
    raza = StringField('Raza', [validators.DataRequired()])
    contacto = StringField('Contacto', [validators.DataRequired()])
    direccion = StringField('Direccion', [validators.DataRequired()])
    descripcion = TextAreaField('Descripcion', [validators.DataRequired()])
    fecha = DateField('Fecha de extravio de la mascota', format='%Y-%m-%d', validators=[validators.DataRequired()])
    
    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image_2 = FileField('Image 2', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image_3 = FileField('Image 3', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    
    
class AddModeloForm(FlaskForm):
    mascota = SelectField('Mascota', validators=[DataRequired()], coerce=int)
    imagenes = FileField('Imágenes', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'])], 
                        render_kw={'multiple': True})
    submit = SubmitField('Agregar Imágenes')