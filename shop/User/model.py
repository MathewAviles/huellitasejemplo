from shop import db, app , LoginManager, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def user_loader(user_id):
    return RegistroU.query.get(user_id)

class RegistroU(db.Model, UserMixin):
    # __tablename__ = 'registro_u' 
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=False)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    telefono = db.Column(db.String(10), unique=True)  
    password = db.Column(db.String(50), unique=False)
    profile = db.Column(db.String(200), unique=False, default='profile.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # # Relación inversa con la tabla Addmascota
    # mascotass = db.relationship('Addmascota', backref=db.backref('usuario', lazy=True))
    
    
    def __repr__(self):
        return '<RegistroU %r>' % self.nombre

#db.create_all()

with app.app_context():
    db.create_all()