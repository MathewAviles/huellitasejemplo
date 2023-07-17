from shop import db,app


class usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique=False, nullable=False)
    correo = db.Column(db.String,unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return '<usuario %r>' % self.nombre

#db.create_all()

with app.app_context():
    db.create_all()