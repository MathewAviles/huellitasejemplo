from flask import Flask
from shop import db,app
from datetime import datetime  
from shop.User.model import RegistroU
from datetime import datetime
import pytz

# Crear un objeto de zona horaria para la zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')

# Obtener la fecha y hora actuales en la zona horaria de Ecuador
pub_date = datetime.now(ecuador_tz)



class Tipo_m(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    tipo_m = db.Column(db.String(50), nullable=False, unique=True)
    def __repr2__(self):
        return '<Tipo_m %r>' % self.tipo_m
    
class Sexo_m(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    sexo_m = db.Column(db.String(50), nullable=False, unique=True)
    def __repr1__(self):
        return '<Sexo_m %r>' % self.sexo_m


class Ubicacion_m(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    ubicacion_m = db.Column(db.String(50), nullable=False, unique=True)
    def __repr3__(self):
        return '<Ubicacion_m %r>' % self.ubicacion_m
    
    
class Estado_m(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    estado_m = db.Column(db.String(50), nullable=False, unique=True)
    def __repr5__(self):
        return '<Estado_m %r>' % self.estado_m
        


class Addmascota(db.Model):
    __seachbale__ = ['nombre', 'descripcion']
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    raza = db.Column(db.String(20), nullable=False)
    contacto = db.Column(db.String(10), nullable=False)
    direccion = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(150), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.now(ecuador_tz))

    sexo_id = db.Column(db.Integer, db.ForeignKey('sexo_m.id'), nullable=False)
    sexo = db.relationship('Sexo_m',backref=db.backref('sexos', lazy=True))
    
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo_m.id'), nullable=False)
    tipo = db.relationship('Tipo_m',backref=db.backref('tipos', lazy=True))
    
    ubicacion_id = db.Column(db.Integer, db.ForeignKey('ubicacion_m.id'), nullable=False)
    ubicacion = db.relationship('Ubicacion_m',backref=db.backref('ubicaciones', lazy=True))
    
    estado_id = db.Column(db.Integer, db.ForeignKey('estado_m.id'), nullable=False)
    estado = db.relationship('Estado_m',backref=db.backref('estados', lazy=True))
    
    user_id = db.Column(db.Integer, db.ForeignKey('registro_u.id'), nullable=False)
    user = db.relationship('RegistroU', backref=db.backref('mascotas', lazy=True))


    image_1 = db.Column(db.String(150), nullable=False, default= 'image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default= 'image.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default= 'image.jpg')
    
    def __repr__(self):
        return '<Addmascota %r>' % self.nombre
    
    
    


        
with app.app_context():
    db.create_all()   
    
#########Formulario  DE IMÁGENES para el reconocimiento############
class Formulario_r(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    
    addmascota_id = db.Column(db.Integer, db.ForeignKey('addmascota.id'), nullable=False)
    addmascota = db.relationship('Addmascota', backref=db.backref('formularios', lazy=True))


    nombre= db.Column(db.String(20), nullable=False, unique=False)
    image_1 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_2 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_3 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_4 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_5 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_6 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_7 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_8 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_9 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_10 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_11 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_12 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_13 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_14 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_15 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_16 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_17 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_18 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_19 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_20 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_21 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_22 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_23 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_24 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_25 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_26 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_27 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_28 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_29 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    image_30 = db.Column(db.String(250), nullable=False, default= 'image.jpg')
    

    
    def __repr7__(self):
        return '<Formulario_r %r>' % self.nombre
    

class RegistroReconocimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    usuario_id = db.Column(db.Integer, db.ForeignKey('registro_u.id'), nullable=True)
    mascota_id = db.Column(db.Integer, db.ForeignKey('addmascota.id'), nullable=True)
    nombre_usuario = db.Column(db.String(50), nullable=False)
    nombre_mascota = db.Column(db.String(20), nullable=False)
    telefono_usuario = db.Column(db.String(10), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr8__(self):
        return '<RegistroReconocimiento %r>' % self.id
    
    
with app.app_context():
    db.create_all()  
    
